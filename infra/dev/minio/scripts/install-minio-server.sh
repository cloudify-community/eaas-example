#!/bin/bash -e

curl -L -o /tmp/minio https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x /tmp/minio
sudo mv /tmp/minio /usr/local/bin/
