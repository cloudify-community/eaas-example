#!/usr/env/bin python

from cloudify import ctx
from cloudify.state import ctx_parameters

CENTOS_7_US_EAST = 'ami-0affd4508a5d2481b'

resource_prefix = ctx_parameters['resource_prefix']
env_type = ctx_parameters['env_type']
vpc_deployment_id = ctx_parameters['vpc_deployment_id']
db_master_username = ctx_parameters['db_master_username']
db_master_password = ctx_parameters['db_master_password']
aws_region = ctx_parameters['aws_region']

configuration = {
    'k8s': {
        'inputs': {}
    },
    'db': {
        'inputs': {}
    },
    's3': {
        'inputs': {
            'bucket_name': '{}bucket'.format(resource_prefix)
        }
    }
}

if env_type == 'dev':
    configuration['k8s']['blueprint'] = 'minikube'
    configuration['db']['blueprint'] = 'vm_with_psql'
    configuration['s3']['blueprint'] = 'minio'
    configuration['s3']['inputs'].update({
        'bucket_region': 'us-west-1'
    })

    for component in ['k8s', 'db', 's3']:
        configuration[component]['inputs'].update({
            'vpc_deployment_id': vpc_deployment_id,
            'resource_prefix': "{}-{}".format(resource_prefix, component),
            'ami_id': CENTOS_7_US_EAST,
            'instance_type': 't2.medium'
        })
elif env_type == 'production':
    configuration['k8s']['blueprint'] = 'eks'
    configuration['k8s']['inputs'].update({
        'resource_suffix': resource_prefix,
        'availability_zone_1': '{}a'.format(aws_region),
        'availability_zone_2': '{}b'.format(aws_region)
    })
    configuration['db']['blueprint'] = 'rds_psql'
    configuration['db']['inputs'].update({
        'vpc_deployment_id': vpc_deployment_id,
        'resource_prefix': "{}-db".format(resource_prefix),
        'stack_name': '{}stack'.format(resource_prefix),
        'db_name': '{}rdsdb'.format(resource_prefix)
    })
    configuration['s3']['blueprint'] = 's3'
    configuration['s3']['inputs']['bucket_region'] = 'us-east-2'
else:
    raise Exception("Unhandled environment type: {}".format(env_type))

configuration['db']['inputs'].update({
    'master_username': db_master_username,
    'master_password': db_master_password
})

for component in ['k8s', 'db', 's3']:
    configuration[component]['inputs'].update({
        'aws_region_name': aws_region
    })

ctx.instance.runtime_properties.update(configuration)
