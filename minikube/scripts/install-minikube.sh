#!/bin/bash -e

curl -L -o /tmp/minikube.rpm https://storage.googleapis.com/minikube/releases/latest/minikube-latest.x86_64.rpm
sudo yum -y install /tmp/minikube.rpm
