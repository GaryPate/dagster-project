# Dagster libraries to run both dagster-webserver and the dagster-daemon. Does not
# need to have access to any pipeline code.

FROM python:3.10-slim



# RUN pip install \
#     dagster \
#     dagster-graphql \
#     dagster-webserver \
#     dagster-postgres \
#     dagster-docker

# Set $DAGSTER_HOME and copy dagster instance and workspace YAML there
ENV DAGSTER_HOME=/opt/dagster/dagster-project/

# RUN mkdir -p $DAGSTER_HOME

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

RUN apt-get update -y && apt-get install -y 
RUN pip3 install -r requirements.txt
RUN python -m textblob.download_corpora 

EXPOSE 3000

CMD ["dagster-webserver", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]