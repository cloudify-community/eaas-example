#!/bin/bash -e

sudo su - docker -c "minikube start --apiserver-ips ${HOST_VM_IP}"
sudo su - docker -c "nohup minikube tunnel &> /dev/null &"
