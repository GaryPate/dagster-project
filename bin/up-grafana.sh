#! /bin/bash

# Create required mounts and volumes if they dont exist
if [ ! -d /mnt/grafana]; then
  mkdir -p /mnt/grafana;
fi

VOLUME = docker volume ls -f name=grafana-storage
if [ ! -z "$VOLUME" ]; 
  then docker volume create grafana-storage
fi