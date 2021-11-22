import os
from dataclasses import dataclass
import pytest
from pyspark.sql import SparkSession
import pydbr
from pydbr.connection import DatabricksConnection

@dataclass
class PydbrTestFixture:
    ENV_VAR_DATABRICKS_TOKEN: str = 'DATABRICKS_BEARER_TOKEN'
    ENV_VAR_DATABRICKS_URL: str = 'DATABRICKS_URL'
    ENV_VAR_DATABRICKS_CLUSTER_ID: str = 'DATABRICKS_CLUSTER_ID'

    dastabricks_token: str = None
    databricks_url: str = None
    databricks_cluster_id: str = None

    dbfs_tmp = '/pydbr-test/tmp'
    dbfs_fix = '/pydbr-test/fixture'
    dbfs_fix_files = '/pydbr-test/fixture/files'

    ws_fix = '/pydbr-test-fixtures/fixture'

    def __post_init__(self):
        self.databricks_url = os.environ[self.ENV_VAR_DATABRICKS_URL]
        self.dastabricks_token = os.environ[self.ENV_VAR_DATABRICKS_TOKEN]
        self.databricks_cluster_id = os.environ[self.ENV_VAR_DATABRICKS_CLUSTER_ID]


@pytest.fixture(scope="session")
def pydbr_fix():
    """Returns Pydbr test fixture."""
    fixture = PydbrTestFixture()
    yield fixture

@pytest.fixture
def dbc(pydbr_fix) -> DatabricksConnection:
    """Databricks connection fixture."""
    connection = pydbr.connect(
        bearer_token=pydbr_fix.dastabricks_token,
        url=pydbr_fix.databricks_url,
        cluster_id=pydbr_fix.databricks_cluster_id)
    yield connection

@pytest.fixture(scope="session")
def spark():
    import os
    os.environ['SPARK_LOCAL_IP'] = '127.0.0.1'
    spark_session = (SparkSession
        .builder
        .appName('TestingPysparkMe')
        .master('local[*]')
        .enableHiveSupport()
        .getOrCreate())
    spark_session.sparkContext.setLogLevel('ERROR')
    yield spark_session
    try:
        spark_session.stop()
    except:
        pass

