#!/bin/bash -e

sudo adduser docker -g docker
echo "docker ALL=(ALL) NOPASSWD:ALL" >> docker-user
sudo chmod 440 docker-user
sudo chown root:root docker-user
sudo mv docker-user /etc/sudoers.d/docker-user
