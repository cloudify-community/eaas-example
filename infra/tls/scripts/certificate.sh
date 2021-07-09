#!/bin/sh
set -e
sudo yum -y install epel-release
sudo yum -y install snapd
sudo systemctl enable --now snapd.socket
sudo ln -s /var/lib/snapd/snap /snap
sudo snap install core || true
sudo snap refresh core || true
sudo yum remove certbot || true
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot certonly --standalone --register-unsafely-without-email --agree-tos -d ${domain}
cert=`sudo cat /etc/letsencrypt/live/${domain}/fullchain.pem`
key=`sudo cat /etc/letsencrypt/live/${domain}/privkey.pem`
cert_base64=`sudo cat /etc/letsencrypt/live/${domain}/fullchain.pem | base64 | tr -d "\n"`
key_base64=`sudo cat /etc/letsencrypt/live/${domain}/privkey.pem | base64 | tr -d "\n"`
ctx instance runtime-properties 'cert' "${cert}"
ctx instance runtime-properties 'key' "${key}"
ctx instance runtime-properties 'cert_base64' "${cert_base64}"
ctx instance runtime-properties 'key_base64' "${key_base64}"