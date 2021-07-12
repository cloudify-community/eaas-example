#!/bin/sh
set -e
sudo rm -rf /etc/letsencrypt
sudo rm -rf /usr/bin/certbot
sudo snap remove certbot
sudo rm -rf /snap
sudo yum -y remove snapd
