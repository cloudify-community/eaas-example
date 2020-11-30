#!/bin/bash -e

data_dir=$(ctx node properties data_dir)

sudo mkdir -p ${data_dir}
sudo adduser minio
sudo chown -R minio:minio ${data_dir}
