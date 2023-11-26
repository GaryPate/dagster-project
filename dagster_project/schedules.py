from dagster import ScheduleDefinition, DefaultScheduleStatus, RunConfig, define_asset_job
from dagster_project.jobs import sentimax_compute_job
from dagster_dbt import build_schedule_from_dbt_selection, build_dbt_asset_selection
from dagster_project.assets.get_dbt_assets import dagster_dbt_assets

HOURLY_PLUS = " {} * * * * "

sentimax_compute_schedule = ScheduleDefinition(job=sentimax_compute_job, 
                                               cron_schedule=HOURLY_PLUS.format('0'),
                                               execution_timezone="Australia/Sydney",
                                               #default_status=DefaultScheduleStatus.RUNNING
                                               )

dbt_assets_select = build_dbt_asset_selection(
    [dagster_dbt_assets], 
    dbt_select="tag:sentimax-dbt"
).downstream()

sentimax_dbt_assets_schedule = ScheduleDefinition(
    job=define_asset_job("dbt_assets_select", selection=dbt_assets_select),
    cron_schedule=HOURLY_PLUS.format('7'),
    execution_timezone="Australia/Sydney",
    #default_status=DefaultScheduleStatus.RUNNING
)