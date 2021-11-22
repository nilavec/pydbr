import pytest
import pydbr


def test_runs_ls_returns_DatabricksRunList(dbc):
    actual = dbc.jobs.runs.ls(offset=1, 
                              limit=100,
                              completed_only=True)
    assert isinstance(actual, pydbr.databricks_data_classes.DatabricksRunList)

def test_runs_ls_for_active_only_returns_DatabricksRunList(dbc):
    actual = dbc.jobs.runs.ls(offset=1, 
                              limit=100,
                              active_only=True)
    assert isinstance(actual, pydbr.databricks_data_classes.DatabricksRunList)


def test_runs_submit_wait_scenario(dbc, pydbr_fix):
    path = f'{pydbr_fix.ws_fix}/HelloPydbr'
    run_id = dbc.jobs.runs.submit_notebook(path, params={'ping':'pong'})
    assert isinstance(run_id, int)

    run = dbc.jobs.runs.get(run_id)
    assert isinstance(run, pydbr.databricks_data_classes.DatabricksRun)
    assert run.run_id == run_id

    dbc.jobs.runs.wait(run_id)
    run_output = dbc.jobs.runs.get_output(run_id)
    # assert parameters are passed
    assert run_output.metadata.task['notebook_task']['base_parameters'] == { 'ping': 'pong' }
    # assert output is correct
    assert run_output.notebook_output.result == 'The answer is: pong'

    export = dbc.jobs.runs.export(run_id)
    assert isinstance(export, pydbr.databricks_data_classes.DatabricksViewList)
    assert len(export.views) > 0
    assert len(export.views[0].content) > 100

    notebook_exports = export.notebooks
    assert len(notebook_exports) > 0
    assert len(notebook_exports[0].content) > 100
