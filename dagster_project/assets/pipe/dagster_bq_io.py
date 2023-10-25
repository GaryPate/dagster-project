from dagster_gcp_pandas import BigQueryPandasIOManager

from dagster import Definitions


import pandas as pd
import json
from dagster import asset


defs = Definitions(
    assets=[twitter_data],
    resources={
        "io_manager": BigQueryPandasIOManager(
            project="ml-dev",  # required
            location="australia-southeast1",  # optional, defaults to the default location for the project - see https://cloud.google.com/bigquery/docs/locations for a list of locations
            dataset="SENTIMAX",  # optional, defaults to PUBLIC
            timeout=15.0,  # optional, defaults to None
        )
    },
)




@asset
def twitter_data() -> pd.DataFrame:

    data = []

    with open("tweet_data.json", 'r', encoding='utf-8') as f:
        for line in f:
            data.append(line)

    df = pd.DataFrame(json.loads(line)[0] for line in data)

    return df

