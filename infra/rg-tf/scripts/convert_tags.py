#!/usr/bin/env python

from cloudify import ctx
from cloudify.state import ctx_parameters

for key in ['rg_tags', 'vn_tags', 'subnet_1_tags', 'subnet_2_tags']:
    ctx.instance.runtime_properties[key] = {
        item['Key']: item['Value'] for item in ctx_parameters[key]
    }
