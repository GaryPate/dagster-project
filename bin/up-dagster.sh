#! /bin/bash

# Create required mounts and volumes if they dont exist
if [ ! -d /mnt/sentimax]; then
  mkdir -p /mnt/sentimax;
fi

if [ ! -d /mnt/gcloud]; then
  mkdir -p /mnt/gcloud;
fi

# Concatenates and stores GCP credentials as required by Dagster
export GCP_CREDS_JSON_CREDS_BASE64="$(cat /mnt/gcloud/application_default_credentials.json | base64)"