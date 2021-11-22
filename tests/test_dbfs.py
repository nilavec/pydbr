import time
import pytest
import pydbr

def test_dbfs_ls(dbc, pydbr_fix):
    actual = dbc.dbfs.ls(pydbr_fix.dbfs_fix_files)
    assert isinstance(actual, list)
    assert 1, len(actual)

    hello_info = actual[0]
    assert isinstance(hello_info, pydbr.databricks_data_classes.DatabricksFileInfo)
    assert f'{pydbr_fix.dbfs_fix_files}/hello.txt' == hello_info.path


def test_dbfs_info(dbc, pydbr_fix):
    actual = dbc.dbfs.info(pydbr_fix.dbfs_fix_files)
    assert isinstance(actual, pydbr.databricks_data_classes.DatabricksFileInfo)
    assert pydbr_fix.dbfs_fix_files == actual.path
    assert True == actual.is_dir
 
def test_dbfs_exists_for_existing_directory_returns_true(dbc, pydbr_fix):
    actual = dbc.dbfs.exists(f'{pydbr_fix.dbfs_fix_files}')
    assert True == actual

def test_dbfs_exists_for_existing_file_returns_true(dbc, pydbr_fix):
    actual = dbc.dbfs.exists(f'{pydbr_fix.dbfs_fix_files}/hello.txt')
    assert True == actual

def test_dbfs_exists_for_missing_file_returns_false(dbc, pydbr_fix):
    actual = dbc.dbfs.exists(f'{pydbr_fix.dbfs_fix_files}/who-am-i.txt')
    assert False == actual


def test_dbfs_read_small_file_returns_file_bytes(dbc, pydbr_fix):
    actual = dbc.dbfs.read(f'{pydbr_fix.dbfs_fix_files}/hello.txt')
    assert actual == b'Hello pydbr!'

def test_dbfs_read_missing_file_raises_exception(dbc, pydbr_fix):
    with pytest.raises(pydbr.common.DatabricksLinkException) as excinfo:
        actual = dbc.dbfs.read(f'{pydbr_fix.dbfs_fix_files}/who-am-i.txt')
    assert excinfo.value.error_code == 'RESOURCE_DOES_NOT_EXIST'


def test_dbfs_read_with_offset_and_lengt_returns_chunk(dbc, pydbr_fix):
    actual = dbc.dbfs.read(f'{pydbr_fix.dbfs_fix_files}/hello.txt',
            offset=3, length=2)
    assert actual == b'lo'

def test_dbfs_read_all_returns_file_bytes(dbc, pydbr_fix):
    actual = dbc.dbfs.read_all(f'{pydbr_fix.dbfs_fix_files}/hello.txt')
    assert actual == b'Hello pydbr!'


def test_dbfs_mkdirs_creates_directories(dbc, pydbr_fix):
    path = f'{pydbr_fix.dbfs_tmp}/some/dir/{pydbr.common.random_id(5, "pydbr-"+str(time.time()))}'    
    actual = dbc.dbfs.mkdirs(path)
    
    assert actual == {}
    assert dbc.dbfs.exists(path) == True

def test_rm_existing_file_path_deletes_it(dbc, pydbr_fix):
    path = f'{pydbr_fix.dbfs_tmp}/some/dir/{pydbr.common.random_id(5, "pydbr-"+str(time.time()))}'    
    dbc.dbfs.mkdirs(path)
    assert dbc.dbfs.exists(path) == True
    
    actual = dbc.dbfs.rm(f'{pydbr_fix.dbfs_tmp}', recursive=True)
    assert dbc.dbfs.exists(pydbr_fix.dbfs_tmp) == False
