#!/bin/bash
set -e

TOKEN="$DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"
ORG="$DOCKER_INFLUXDB_INIT_ORG"

BUCKETS=("$BUCKET_ROBOT")

for bucket in "${BUCKETS[@]}"; do
    echo "Creating bucket $bucket ..."
    influx bucket create \
        --name "$bucket" \
        --org "$ORG" \
        --token "$TOKEN"
done
