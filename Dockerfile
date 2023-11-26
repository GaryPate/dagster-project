# Dagster libraries to run both dagster-webserver and the dagster-daemon. Does not
# need to have access to any pipeline code.

FROM python:3.10-slim

ARG PGPASS
ARG PGUSER
ARG BEARER
ARG DAGSTER_IMAGE

ENV BEARER_TOKEN=${BEARER}
ENV DAGSTER_POSTGRES_DB=dagsterdb
ENV DAGSTER_POSTGRES_PASSWORD=${PGPASS} 
ENV DAGSTER_POSTGRES_USER=${PGUSER}
ENV DAGSTER_CURRENT_IMAGE=${DAGSTER_IMAGE}
ENV POSTGRES_DB=dagsterdb 
ENV POSTGRES_PASSWORD=${PGPASS}
ENV POSTGRES_USER=${PGUSER}

ENV DAGSTER_HOME=/opt/dagster/dagster-project/
ENV DBT_TARGET_PATH=/opt/dagster/dagster-project/dbt_project/target/
ENV DBT_PROFILES_DIR=/opt/dagster/dagster-project/dbt_project/
ENV GOOGLE_APPLICATION_CREDENTIALS=/mnt/gcloud/dagster_gcp_key.json
ENV GCP_PROJECT=ml-dev-403200

WORKDIR $DAGSTER_HOME

COPY dagster.yaml workspace.yaml requirements.txt $DAGSTER_HOME
COPY dagster_project ./dagster_project
COPY dbt_project ./dbt_project
COPY requirements.txt .
COPY bin/ bin/
RUN apt-get update -y && apt-get install -y && \
    pip3 install -r requirements.txt && \ 
    python -m textblob.download_corpora 

EXPOSE 3000
EXPOSE 4000
