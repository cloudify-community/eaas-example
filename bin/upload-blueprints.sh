#!/bin/bash -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Uploading application blueprint..."
# cfy blueprints upload ${script_dir}/../app/aws-blueprint.yaml -b aws_app &
# cfy blueprints upload ${script_dir}/../app/azure-blueprint.yaml -b azure_app &
cfy blueprints upload ${script_dir}/../app/blueprint.yaml -b app &

echo "Uploading VPC blueprint..."
cfy blueprints upload ${script_dir}/../infra/vpc/blueprint.yaml -b vpc &

echo "Uploading RG blueprint..."
cfy blueprints upload ${script_dir}/../infra/network/azure-blueprint.yaml -b rg &

for env_type in dev prod
do
  find ${script_dir}/../infra/${env_type}/* -prune -type d | while IFS= read -r d; do
    blueprint_id=$(basename ${d})
    echo "Uploading ${blueprint_id} blueprints..."
    cfy blueprints upload ${d}/blueprint.yaml -b ${blueprint_id} || \
      echo "No blueprint.yaml in ${d}... Moving forward." &
    cfy blueprints upload ${d}/aws-blueprint.yaml -b aws_${blueprint_id} || \
      echo "No aws-blueprint.yaml in ${d}... Moving forward." &
    cfy blueprints upload ${d}/azure-blueprint.yaml -b azure_${blueprint_id} || \
      echo "No azure-blueprint.yaml in ${d}... Moving forward." &
  done
done
