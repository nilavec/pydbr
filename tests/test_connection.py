import pydbr

def test_connect_returns_connection(pydbr_fix):
    dbc = pydbr.connect(
        bearer_token=pydbr_fix.dastabricks_token,
        url=pydbr_fix.databricks_url,
        cluster_id=pydbr_fix.databricks_cluster_id)

    assert isinstance(dbc, pydbr.connection.DatabricksConnection)

def test_connect_with_trailing_slash_for_url_removes_slash(pydbr_fix):
    dbc = pydbr.connect(
        bearer_token=pydbr_fix.dastabricks_token,
        url=pydbr_fix.databricks_url + '/',
        cluster_id=pydbr_fix.databricks_cluster_id)

    assert isinstance(dbc, pydbr.connection.DatabricksConnection)
    assert dbc.link.url == pydbr_fix.databricks_url
 

def test_connection_property_link_is_a_Link(dbc):
    assert hasattr(dbc, 'link')
    assert isinstance(dbc.link, pydbr.common.Link)

def test_connection_property_worksapce_is_a_Workspace(dbc):
    assert hasattr(dbc, 'workspace')
    assert isinstance(dbc.workspace, pydbr.workspace.Workspace)

def test_connection_property_dbfs_is_a_DBFS(dbc):
    assert hasattr(dbc, 'dbfs')
    assert isinstance(dbc.dbfs, pydbr.dbfs.DBFS)

def test_connection_property_jobs_is_a_Jobs(dbc):
    assert hasattr(dbc, 'jobs')
    assert isinstance(dbc.jobs, pydbr.jobs.Jobs)

