from dagster import Definitions, load_assets_from_modules, define_asset_job, AssetSelection, FilesystemIOManager
from dagster_gcp import BigQueryResource
from dagster_project.assets import semx_assets, get_dbt_assets
import os
import json 
import base64
from dagster_gcp_pandas import BigQueryPandasIOManager
from dagster_dbt import DbtCliResource, build_schedule_from_dbt_selection
from dagster_project.constants import DBT_PROJECT_DIR


from dagster import (
    Definitions,
    EnvVar
)

AUTH_FILE = "./gcp_creds.json"

with open(AUTH_FILE, "w") as f:
    json.dump(json.loads(base64.b64decode(os.getenv("GCP_CREDS_JSON_CREDS_BASE64"))), f)

os.environ["GCP_PROJECT"] = 'ml-dev-403200'

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = AUTH_FILE

all_assets = load_assets_from_modules([semx_assets, 
                                       get_dbt_assets
                                       ])

sentimax_compute_job = define_asset_job("sentimax_compute_job", selection=AssetSelection.groups("sentimax_compute"))

# sentimax_dbt_job = define_asset_job(
#     name="sentimax_dbt_job",
#     selection=AssetSelection.groups('sentimax_dbt')
#     # tags={
#     #     "job": "sentimax_dbt_job"
#     # },
# )


sentimax_dbt_assets_schedule = build_schedule_from_dbt_selection(
    [get_dbt_assets.dagster_dbt_assets],
    job_name="dbt_model_job",
    cron_schedule="@daily",
    dbt_select="tag:sentimax-dbt",
)

defs = Definitions(
    assets=all_assets,
    jobs=[sentimax_compute_job],
    schedules=[sentimax_dbt_assets_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR),
        "bigquery": BigQueryResource(
            project=EnvVar("GCP_PROJECT"),  # required
            dataset="SENTIMAX",
            #gcp_credentials=EnvVar("GOOGLE_APPLICATION_CREDENTIALS"),
         ),
        "io_manager": BigQueryPandasIOManager(project=EnvVar("GCP_PROJECT"),
                                              dataset="SENTIMAX")

    },
)


# all_assets_job = define_asset_job(name="sentimax_job")
# asset1_job = define_asset_job(name="asset1_job", selection="asset1")

# defs = Definitions(
#     assets=[],
#     jobs=[all_assets_job, asset1_job],
# )