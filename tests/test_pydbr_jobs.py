import pytest
import pydbr

def test_jobs_list_returns_list(dbc, pydbr_fix):
    actual = dbc.jobs.list()
    assert isinstance(actual, list)


def test_jobs_has_runs_property(dbc):
    assert hasattr(dbc.jobs, 'runs')
    assert isinstance(dbc.jobs.runs, pydbr.runs.Runs)
