#!/usr/bin/python

from cloudify import ctx

ctx.instance.runtime_properties['index_content'] = \
    ctx.get_resource(ctx.node.properties.get('index_file_path')).decode()