from dagster import define_asset_job, AssetSelection

sentimax_compute_job = define_asset_job("sentimax_compute_job", selection=AssetSelection.groups("sentimax_compute"))
