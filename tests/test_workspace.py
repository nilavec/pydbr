import pytest
import pydbr

def test_workspace_ls_existing_directory_retuns_list_of_items(dbc, pydbr_fix):
    path = pydbr_fix.ws_fix
    actual = dbc.workspace.ls(path)
    assert isinstance(actual, list)
    assert len(actual) == 1
    
    item_info = actual[0]
    assert isinstance(item_info, pydbr.databricks_data_classes.DatabricksObjectInfo)

def test_workspace_ls_missing_directory_raises_exception(dbc, pydbr_fix):
    path = f'{pydbr_fix.ws_fix}/who/am/i' 
    with pytest.raises(pydbr.common.DatabricksLinkException) as excinfo:
        actual = dbc.workspace.ls(path)
    assert excinfo.value.error_code == 'RESOURCE_DOES_NOT_EXIST'

def test_exists_for_root_returns_true(dbc, pydbr_fix):
    assert dbc.workspace.exists('/') == True

def test_exists_for_existing_directory_returns_true(dbc, pydbr_fix):
    assert dbc.workspace.exists(pydbr_fix.ws_fix) == True

def test_exists_for_missing_directory_returns_false(dbc, pydbr_fix):
    assert dbc.workspace.exists(f'{pydbr_fix.ws_fix}/who/am/i') == False

def test_is_directory_for_root_directory_returns_true(dbc, pydbr_fix):
    assert dbc.workspace.is_directory('/') == True

def test_is_directory_for_existing_directory_returns_true(dbc, pydbr_fix):
    assert dbc.workspace.is_directory(pydbr_fix.ws_fix) == True

def test_is_directory_for_existing_notebook_returns_false(dbc, pydbr_fix):
    assert dbc.workspace.is_directory(f'{pydbr_fix.ws_fix}/HelloPydbr') == False


def test_is_directory_for_missing_item_raises_exception(dbc, pydbr_fix):
    with pytest.raises(pydbr.common.DatabricksLinkException) as excinfo:
        dbc.workspace.is_directory(f'{pydbr_fix.ws_fix}/who/am/i')
    assert excinfo.value.error_code == 'RESOURCE_DOES_NOT_EXIST'


def test_export_for_notebook_returns_content_bytes(dbc, pydbr_fix):
    path = f'{pydbr_fix.ws_fix}/HelloPydbr'
    actual = dbc.workspace.export(path)
    assert "print(" in actual.decode()

def test_export_source_format_as_string_can_be_mixed_case(dbc, pydbr_fix):
    path = f'{pydbr_fix.ws_fix}/HelloPydbr'
    actual = dbc.workspace.export(path, format='SoUrCe')
    assert "print(" in actual.decode()

def test_export_for_missing_item_raises_exception(dbc, pydbr_fix):
    path = f'{pydbr_fix.ws_fix}/who/am/i'
    with pytest.raises(pydbr.common.DatabricksLinkException) as excinfo:
        ctual = dbc.workspace.export(path, format='SOURCE')
    assert excinfo.value.error_code == 'RESOURCE_DOES_NOT_EXIST'


