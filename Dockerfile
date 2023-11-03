# Dagster libraries to run both dagster-webserver and the dagster-daemon. Does not
# need to have access to any pipeline code.

FROM python:3.10-slim



# RUN pip install \
#     dagster \
#     dagster-graphql \
#     dagster-webserver \
#     dagster-postgres \
#     dagster-docker
ARG PGPASS
ARG PGUSER
ARG BEARER

ENV DAGSTER_POSTGRES_DB=dagsterdb
ENV DAGSTER_POSTGRES_PASSWORD=${PGPASS} 
ENV DAGSTER_POSTGRES_USER=${PGUSER}
ENV POSTGRES_PASSWORD=${PGPASS}
ENV BEARER_TOKEN=${BEARER}

# Set $DAGSTER_HOME and copy dagster instance and workspace YAML there
ENV DAGSTER_HOME=/opt/dagster/dagster-project/
ENV DBT_TARGET_PATH=/opt/dagster/dagster-project/dbt_project/target/
ENV DBT_PROFILES_DIR=/opt/dagster/dagster-project/dbt_project/
ENV GOOGLE_APPLICATION_CREDENTIALS=/mnt/gcloud/dagster_gcp_key.json

COPY dagster.yaml workspace.yaml $DAGSTER_HOME

WORKDIR $DAGSTER_HOME

# Copy our code and workspace to /usr/src/app
# COPY dagster.yaml workspace.yaml .
COPY dagster_project ./dagster_project
COPY dbt_project ./dbt_project
COPY pyproject.toml .
COPY setup.cfg .
COPY setup.py .
COPY requirements.txt .
COPY up.sh .

RUN apt-get update -y && apt-get install -y 
RUN pip3 install -r requirements.txt
RUN python -m textblob.download_corpora 
RUN mkdir /mnt/gcloud/
# RUN mkdir /mnt/dbt/

EXPOSE 3100

# CMD ["mkdir" "/mnt/gcloud/"]
# CMD ["mkdir" "/mnt/dbt/"]

# CMD ["dagster-webserver", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]