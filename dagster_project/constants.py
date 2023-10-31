from dagster_dbt import DbtCliResource
from dagster import file_relative_path

DBT_PROJECT_DIR = file_relative_path(__file__, "../dbt_project")

dbt_resource = DbtCliResource(project_dir=DBT_PROJECT_DIR)
dbt_parse_invocation = dbt_resource.cli(["parse"]).wait()
dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")
