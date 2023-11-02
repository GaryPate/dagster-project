#! /bin/bash

export GCP_CREDS_JSON_CREDS_BASE64="$(cat /mnt/gcloud/application_default_credentials.json | base64)"