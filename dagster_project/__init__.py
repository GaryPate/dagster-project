from dagster import Definitions, load_assets_from_modules, define_asset_job, AssetSelection, ScheduleDefinition
from dagster_gcp import BigQueryResource
from dagster_project.assets import semx_assets, get_dbt_assets
import os
import json 
import base64
from dagster_gcp_pandas import BigQueryPandasIOManager
from dagster_dbt import DbtCliResource, build_schedule_from_dbt_selection
from dagster_project.constants import DBT_PROJECT_DIR
from dagster import AssetSelection, define_asset_job

HOURLY_PLUS = '{} * * * *'


from dagster import (
    Definitions,
    EnvVar
)

AUTH_FILE = "./gcp_creds.json"

with open(AUTH_FILE, "w") as f:
    json.dump(json.loads(base64.b64decode(os.getenv("GCP_CREDS_JSON_CREDS_BASE64"))), f)

os.environ["GCP_PROJECT"] = 'ml-dev-403200'

all_assets = load_assets_from_modules([semx_assets, 
                                       get_dbt_assets
                                       ])

sentimax_compute_job = define_asset_job("sentimax_compute_job", selection=AssetSelection.groups("sentimax_compute"))

sentimax_compute_schedule = ScheduleDefinition(job=sentimax_compute_job, 
                                               cron_schedule=HOURLY_PLUS.format('0'),
                                               execution_timezone="Australia/Sydney")

sentimax_dbt_assets_schedule = build_schedule_from_dbt_selection(
    [get_dbt_assets.dagster_dbt_assets],
    job_name="dbt_model_job",
    cron_schedule=HOURLY_PLUS.format('10'),
    dbt_select="tag:sentimax-dbt",
    execution_timezone="Australia/Sydney"
)

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
