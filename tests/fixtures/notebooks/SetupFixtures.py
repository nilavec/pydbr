# Databricks notebook source
DBFS_PYDBR_TESTS = '/pydbr-test'
DBFS_PYDBR_TMP = f'{DBFS_PYDBR_TESTS}/tmp'
DBFS_PYDBR_FIXTURES = f'{DBFS_PYDBR_TESTS}/fixture'

dbutils.fs.rm(DBFS_PYDBR_TESTS, recurse=True)
dbutils.fs.mkdirs(DBFS_PYDBR_TMP)
dbutils.fs.mkdirs(DBFS_PYDBR_FIXTURES)

# 
DBFS_PYDBR_FIXTURE_FILES = f'{DBFS_PYDBR_FIXTURES}/files'
dbutils.fs.mkdirs(DBFS_PYDBR_FIXTURE_FILES)
dbutils.fs.put(f'{DBFS_PYDBR_FIXTURE_FILES}/hello.txt', 'Hello pydbr!')

# COMMAND ----------

# MAGIC %sh
# MAGIC ls /dbfs/pydbr-test/tmp/some/dir

# COMMAND ----------

