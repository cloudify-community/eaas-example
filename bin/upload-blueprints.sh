#!/bin/bash -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Uploading application blueprint..."
cfy blueprints upload ${script_dir}/../app/blueprint.yaml -b app

for env_type in dev prod
do
  find ${script_dir}/../infra/${env_type}/* -prune -type d | while IFS= read -r d; do
    blueprint_id=$(basename ${d})
    echo "Uploading blueprint ${blueprint_id}..."
    cfy blueprints upload ${d}/blueprint.yaml -b ${blueprint_id}
  done
done
