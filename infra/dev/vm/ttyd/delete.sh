#!/usr/bin/env bash

sudo systemctl disable ttyd.service

sudo rm /etc/systemd/system/ttyd.service
sudo rm /opt/ttyd
