
from dagster_project.constants import dbt_manifest_path
from dagster import AssetExecutionContext
from dagster_dbt import (
    DbtCliResource,
    dbt_assets,
)


# class DbtConfig(Config):
#     full_refresh: True


@dbt_assets(
    manifest=dbt_manifest_path,
    op_tags={"select":"semx_stg03_tweet_increment"}
)
def dagster_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


# @dbt_assets(
#     manifest=dbt_manifest_path,
#     op_tags={"select":"semx_stg03_tweet_increment"}
# )
# def stg03_tweet_increment(context: AssetExecucleartionContext, dbt: DbtCliResource):
#     yield from dbt.cli(["build"], context=context).stream()



# @dbt_assets(
#     manifest=dbt_manifest_path,
#     op_tags={"select":"semx_stg05_sentiment_increment"}
# )
# def stg05_sentiment_increment(context: AssetExecutionContext, dbt: DbtCliResource):
#     yield from dbt.cli(["build"], context=context).stream()



# @dbt_assets(
#     manifest=dbt_manifest_path,
#     op_tags={"select": "semx_stg05_sentimenet_increment"}
# )
# def dagster_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
#     yield from dbt.cli(["build"], context=context).stream()
    
