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



gcloud auth configure-docker australia-southeast1-docker.pkg.dev

dagster_gcp_key - bigquery service account

application_default_credentials.json

nginx reverse proxy

![System Diagram](https://github.com/GaryPate/dagster-project/assets/20076884/18b14f6f-2910-40fa-85ca-d615a141da10)
