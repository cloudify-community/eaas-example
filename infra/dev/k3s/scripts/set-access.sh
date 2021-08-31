#!/bin/bash -e

sudo chmod 644 /etc/rancher/k3s/k3s.yaml
ctx instance runtime-properties host_addr ${host_addr}
