#!/usr/bin/env bash

curl -L https://github.com/tsl0922/ttyd/releases/download/1.6.3/ttyd.x86_64 -o /tmp/ttyd
chmod 755 /opt/ttyd

sudo mv /tmp/ttyd /opt/ttyd
sudo chown root:root /opt/ttyd
