#!/bin/bash -e

sed -i "/${host_addr} kubernetes/d" /etc/hosts
