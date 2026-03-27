#!/bin/bash
set -e

TOKEN="$DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"
ORG="$DOCKER_INFLUXDB_INIT_ORG"
BUCKET="$BUCKET_ROBOT"

if influx bucket list \
    --name "$BUCKET" \
    --org "$ORG" \
    --token "$TOKEN" \
    --hide-headers | grep -q .; then
    echo "Bucket $BUCKET already exists; skipping seed."
else
    echo "Creating bucket $BUCKET ..."
    influx bucket create \
        --name "$BUCKET" \
        --org "$ORG" \
        --token "$TOKEN"

    echo "Seeding zero motion_intent values into $BUCKET ..."
    influx write \
        --bucket "$BUCKET" \
        --org "$ORG" \
        --token "$TOKEN" \
        "motion_intent v=0,omega=0,emergency_stop=false"
fi
