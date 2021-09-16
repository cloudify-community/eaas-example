#!/usr/bin/env bash

cat << EOF > /tmp/ttyd.service
[Unit]
Description=ttyd
After=network.target
Type=simple
Restart=always
RestartSec=5
User=centos
ExecStart=/opt/ttyd bash

[Install]
WantedBy=multi-user.target
EOF
chmod 644 /tmp/ttyd.service

sudo mv /tmp/ttyd.service /etc/systemd/system/ttyd.service
sudo chown root:root /etc/systemd/system/ttyd.service

sudo systemctl enable ttyd.service

