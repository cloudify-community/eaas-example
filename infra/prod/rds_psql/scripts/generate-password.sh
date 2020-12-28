#!/bin/bash -e

master_password=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c16)
ctx instance runtime-properties master_password ${master_password}
