from dagster import ScheduleDefinition, DefaultScheduleStatus
from dagster_project.jobs import sentimax_compute_job
from dagster_dbt import build_schedule_from_dbt_selection
from dagster_project.assets import get_dbt_assets

HOURLY_PLUS = " {} * * * * "

sentimax_compute_schedule = ScheduleDefinition(job=sentimax_compute_job, 
                                               cron_schedule=HOURLY_PLUS.format('0'),
                                               execution_timezone="Australia/Sydney",
                                               default_status=DefaultScheduleStatus.RUNNING)

sentimax_dbt_assets_schedule = build_schedule_from_dbt_selection(
    [get_dbt_assets.dagster_dbt_assets],
    job_name="dbt_model_job",
    cron_schedule=HOURLY_PLUS.format('10'),
    dbt_select="tag:sentimax-dbt",
    execution_timezone="Australia/Sydney"
)