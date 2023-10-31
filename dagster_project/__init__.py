from dagster import Definitions, load_assets_from_modules
from dagster_gcp import BigQueryResource
from .assets import semx_assets, get_dbt_assets
import os
import json 
import base64

import os
from dagster_gcp_pandas import BigQueryPandasIOManager
from dagster import Definitions
from dagster_dbt import DbtCliResource
from .constants import DBT_PROJECT_DIR
from dagster import Definitions, define_asset_job


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


semx_asset_job = define_asset_job(name="semx_asset_job")



defs = Definitions(
    assets=all_assets,
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