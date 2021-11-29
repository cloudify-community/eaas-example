#!/usr/bin/env python

from cloudify import manager
from cloudify import ctx

try:
    execution_id = ctx.instance.runtime_properties['execution_id']
    if execution_id:
        execution_id = manager.get_rest_client().executions.cancel(execution_id)
except Exception as e:
    ctx.logger.warn(str(e))
