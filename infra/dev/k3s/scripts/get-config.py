#!/usr/bin/env python

from cloudify import ctx
import yaml


with open('/etc/rancher/k3s/k3s.yaml','r') as f:
  ctx.instance.runtime_properties['config'] = yaml.safe_load(f.read().replace(
    '127.0.0.1',
    'kubernetes'))
