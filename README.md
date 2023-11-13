Sentimax - Bitcoin Twitter Sentiment Analysis

This deployment uses the Dagster framework to perform live sentiment analysis on a small sample of Bitcoin tweets from the Twitter (X) API.

It is intended to be viewed as sample code. Full deployment requires subscription to the Basic Twitter API and Google Cloud Platform. 

Nginx is ten used as a reverse proxy to expose the Docker containers to a DNS. 

Both the Dagster UI and a Grafana dashboard are available from these two endpoints.

http://app.sentimax.org/grafana/dashboards
http://app.sentimax.org/dagster

Description

Cloudbuild.yaml 

This controls the Google Gloudbuild CI/CD process. Retrieves GCP secrets and pushes built docker images to artefact repository.  

Python code is located in dagster_project/assets/

semx_assets.py contains the a basic Sentiment Class that returns and parses twitter sentiment using the Tweepy Client for the Twitter (X) API.

The @asset decorator defines to Dagster, functions that return a materializable data source.

get_dbt_assets.py is a context for Dagster that allows DBT models to load into the Dagster UI and framework in general.

schedules.py contains the job schedules for the pyton compute and the DBT-Biguery jobs. 


DBT

The dbt component is a regular dbt project under dbt_project. The queries under models/sentimax_bq/ control loading and incrementing of tables between the host environment and Google BigQuery.


Grafana

Grafana Dashboarding queries the results stored on Big Query

Nginx

The dagster_webserver UI is hosted on port 3000 and the Grafana dasboard showing Bitcoin sentiment over time is on port 3010. The reverse proxy for these are then sent by Nginx to app.sentimax.org at the following paths

/dagster
/grafana/dashboards


Dagster is deployed into several docker images via docker-compose.yaml.

dagster_webserver provides a UI and interface controls for the orchestration.

dagster_daemon is the background service and provides timing for such things as sensors, schedule and run queue.

docker_postgres is used for recording all data related to the framework itself.

dagster_user_code runs in a grpc server that contains the executable code for jobs and is decoupled to allow for separate updates to jobs without having to interrupt the orchestrator.

gcloud auth configure-docker australia-southeast1-docker.pkg.dev

dagster_gcp_key - bigquery service account

application_default_credentials.json

nginx reverse proxy

![System Diagram](https://github.com/GaryPate/dagster-project/assets/20076884/18b14f6f-2910-40fa-85ca-d615a141da10)
