import os
import json 
import base64
from dagster_gcp_pandas import BigQueryPandasIOManager
from dagster_gcp import BigQueryResource
from dagster_dbt import DbtCliResource
from dagster_project.constants import DBT_PROJECT_DIR
from dagster_project.schedules import sentimax_compute_schedule, sentimax_dbt_assets_schedule
from dagster_project.jobs import sentimax_compute_job
from dagster_project.assets import semx_assets, get_dbt_assets
from dagster import Definitions, EnvVar, load_assets_from_modules


all_assets = load_assets_from_modules([semx_assets, get_dbt_assets])

defs = Definitions(
    assets=all_assets,
    jobs=[sentimax_compute_job],
    schedules=[sentimax_dbt_assets_schedule, sentimax_compute_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR),
        "bigquery": BigQueryResource(
            project=EnvVar("GCP_PROJECT"),
            dataset="SENTIMAX",
         ),
        "io_manager": BigQueryPandasIOManager(project=EnvVar("GCP_PROJECT"),
                                              dataset="SENTIMAX")
    },
)
