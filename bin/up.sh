#! /bin/bash

if [ ! -d /mnt/sentimax]; then
  mkdir -p /mnt/sentimax;
fi

if [ ! -d /mnt/grafana]; then
  mkdir -p /mnt/grafana;
fi

if [ ! -d /mnt/gcloud]; then
  mkdir -p /mnt/gcloud;
fi

export GCP_CREDS_JSON_CREDS_BASE64="$(cat /mnt/gcloud/application_default_credentials.json | base64)"