#!/bin/bash -e

data_dir=$(ctx node properties data_dir)
access_key_id=$(ctx node properties access_key_id)
secret_access_key=$(ctx node properties secret_access_key)

sudo su - minio -c "MINIO_ACCESS_KEY=${access_key_id} MINIO_SECRET_KEY=${secret_access_key} nohup minio server ${data_dir} > /dev/null 2>&1 &"
