#!/bin/bash -e

access_key_id=$(ctx node properties access_key_id)
secret_access_key=$(ctx node properties secret_access_key)

mc alias set local http://localhost:9000 ${access_key_id} ${secret_access_key}
