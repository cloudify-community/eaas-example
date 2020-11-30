#!/bin/bash -e

curl -L -o /tmp/mc https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x /tmp/mc
sudo mv /tmp/mc /usr/local/bin/
