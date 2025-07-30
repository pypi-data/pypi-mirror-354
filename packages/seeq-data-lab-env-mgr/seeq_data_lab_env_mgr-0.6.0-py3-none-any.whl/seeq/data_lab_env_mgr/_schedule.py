import os
import json
import requests
import importlib.resources as pkg_resources

from datetime import date
from seeq import spy
from seeq.sdk import ItemsApi, SystemApi, ProjectsApi
from seeq.sdk import ConfigurationOptionInputV1, ConfigurationInputV1, ProjectInputV1

PROJECT_NAME = "com.seeq.data_lab_env_mgr"
PROJECT_TYPE = "DATA_LAB_FUNCTIONS"
PROJECT = "Project"
SCHEDULED_NOTEBOOKS_ENABLED = 'Features/DataLab/ScheduledNotebooks/Enabled'
SCHEDULED_NOTEBOOK_FILENAME = "data_lab_env_mgr_scheduled_job.ipynb"
INTERVAL = "every weekday"
CONFIG_LIMIT = 100000


def _create_project(project_name, project_type):
    projects_api = ProjectsApi(spy.client)
    project_input = ProjectInputV1(name=project_name, folder_id=None, project_type=project_type)
    return projects_api.create_project(body=project_input).id

def _get_or_create_project():
    items_api = ItemsApi(spy.client)
    items_response = items_api.search_items(filters=[f'name=={PROJECT_NAME}'], types=["Project"])
    if items_response.items:
        return items_response.items[0].id
    return _create_project(PROJECT_NAME, PROJECT_TYPE)


def _ensure_scheduled_notebooks_feature_enabled():
    system_api = SystemApi(spy.client)
    configs = system_api.get_configuration_options(limit=CONFIG_LIMIT).configuration_options
    enabled = next(filter(lambda c: c.path == SCHEDULED_NOTEBOOKS_ENABLED, configs), None)
    if not enabled or not enabled.value:
        note = f"Enabled by Data Lab Environment Manager on {date.today()}"
        config_input = ConfigurationInputV1(configuration_options=[
            ConfigurationOptionInputV1(path=SCHEDULED_NOTEBOOKS_ENABLED, value=True, note=note)
        ])
        system_api.set_configuration_options(body=config_input)


def _read_resource_file(module, filename):
    source = pkg_resources.files(module).joinpath(filename)
    with pkg_resources.as_file(source) as eml:
        return eml.read_text()

def _upload_notebook_to_project(file_name, project_id):
    import seeq.data_lab_env_mgr.notebooks
    notebook_content = json.loads(_read_resource_file(seeq.data_lab_env_mgr.notebooks, file_name))

    contents_url = f"{spy.session.private_url}/data-lab/{project_id}/api/contents"
    headers = {**spy.client.default_headers}
    spy.client.add_authorization_header(headers)

    response = requests.put(
        f"{contents_url}/{os.path.basename(file_name)}",
        headers=headers,
        json={
            "name": os.path.basename(file_name),
            "type": "notebook",
            "format": "json",
            "content": notebook_content,
        }
    )
    response.raise_for_status()

def _schedule_job_if_not_scheduled(notebook, project_id, interval):
    notebook_url = f"{spy.session.private_url}/data-lab/{project_id}/notebooks/{notebook}"
    df = spy.jobs.pull(notebook_url, all=True)
    if df is not None and not df.empty:
        return

    spy.jobs.schedule(
        interval,
        datalab_notebook_url=notebook_url,
        notify_on_skipped_execution=False,
        notify_on_automatic_unschedule=False,
        quiet=True
    )

def create_schedule():
    try:
        if spy.user.is_admin and not spy._datalab.is_executor():
            project_id = _get_or_create_project()
            # This will always makes sure the notebook in the scheduled project is up to date
            _upload_notebook_to_project(SCHEDULED_NOTEBOOK_FILENAME, project_id)
            _ensure_scheduled_notebooks_feature_enabled()
            _schedule_job_if_not_scheduled(SCHEDULED_NOTEBOOK_FILENAME, project_id, INTERVAL)
        else:
            #User does not have admin privileges or is a DataLab executor.
            pass
    except Exception as e:
        pass