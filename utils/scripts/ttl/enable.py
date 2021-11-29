#!/usr/bin/env python

import datetime
from cloudify import manager
from cloudify import ctx

SCHEDULE_FORMAT = '%Y-%m-%d %H:%M'

ttl = ctx.node.properties.get('ttl')

ctx.logger.debug("TTL is {}".format(ttl))

if ttl > 0:
    schedule_time = (datetime.datetime.now() + \
                     datetime.timedelta(minutes=ttl)).strftime(
                     SCHEDULE_FORMAT)


    ctx.logger.info("This deployment will be uninstalled at {}".format(schedule_time))
    execution_id = manager.get_rest_client().executions.start(
        deployment_id = ctx.deployment.id,
        workflow_id = "uninstall",
        parameters = {"ignore_failure": True},
        schedule = schedule_time).id

    ctx.instance.runtime_properties['execution_id'] = execution_id
