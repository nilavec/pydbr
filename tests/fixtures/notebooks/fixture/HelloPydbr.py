# Databricks notebook source
dbutils.widgets.text('ping','none')

# COMMAND ----------

dbutils.widgets.help()

# COMMAND ----------

print("I am alive!")

# COMMAND ----------

dbutils.notebook.exit("The answer is: " + dbutils.widgets.get('ping'))

# COMMAND ----------

