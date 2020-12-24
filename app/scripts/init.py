#!/usr/env/bin python

import random
import string

from cloudify import ctx
from cloudify.state import ctx_parameters
from cloudify.exceptions import NonRecoverableError

AWS_RESOURCES = {
    'us-east-1': {
        'ami': 'ami-00e87074e52e6c9f9',
    },
    'us-east-2': {
        'ami': 'ami-00f8e2c955f7ffa9b',
    },
    'us-west-1': {
        'ami': 'ami-08d2d8b00f270d03b',
        'availability_zones': ('a', 'c')
    },
    'us-west-2': {
        'ami': 'ami-0686851c4e7b1a8e1'
    },
    'af-south-1': {
        'ami': 'ami-0b761332115c38669'
    },
    'ap-east-1': {
        'ami': 'ami-09611bd6fa5dd0e3d'
    },
    'ap-south-1': {
        'ami': 'ami-0ffc7af9c06de0077'
    },
    'ap-northeast-1': {
        'ami': 'ami-0ddea5e0f69c193a4'
    },
    'ap-northeast-2': {
        'ami': 'ami-0e4214f08b51e23cc'
    },
    'ap-southeast-1': {
        'ami': 'ami-0adfdaea54d40922b'
    },
    'ap-southeast-2': {
        'ami': 'ami-03d56f451ca110e99'
    },
    'ca-central-1': {
        'ami': 'ami-0a7c5b189b6460115'
    },
    'eu-central-1': {
        'ami': 'ami-08b6d44b4f6f7b279'
    },
    'eu-west-1': {
        'ami': 'ami-04f5641b0d178a27a'
    },
    'eu-west-2': {
        'ami': 'ami-0b22fcaf3564fb0c9'
    },
    'eu-west-3': {
        'ami': 'ami-072ec828dae86abe5'
    },
    'eu-south-1': {
        'ami': 'ami-0fe3899b62205176a'
    },
    'eu-north-1': {
        'ami': 'ami-0358414bac2039369'
    },
    'me-south-1': {
        'ami': 'ami-0ac17dcdd6f6f4eb6'
    },
    'sa-east-1': {
        'ami': 'ami-02334c45dd95ca1fc'
    }
}

COMPONENT_BLUEPRINTS = {
    'network': {
        'dev': 'simple_network',
        'production': 'complex_network'
    },
    'k8s': {
        'dev': 'minikube',
        'production': 'eks'
    },
    'db': {
        'dev': 'vm_with_psql',
        'production': 'rds_psql'
    },
    's3': {
        'dev': 'minio',
        'production': 's3'
    }
}

resource_prefix = ctx_parameters['resource_prefix']
env_type = ctx_parameters['env_type']
db_master_username = ctx_parameters['db_master_username']
db_master_password = ctx_parameters['db_master_password']
aws_region = ctx_parameters['aws_region']

if aws_region not in AWS_RESOURCES:
    raise NonRecoverableError("Unsupported region: {}".format(aws_region))

az1_suffix, az2_suffix = AWS_RESOURCES[aws_region].get('availability_zones', ('a', 'b'))

if not db_master_password:
    db_master_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

if not resource_prefix:
    ctx.logger.info("Resource prefix not provided; will generate one")
    resource_prefix = ''.join(random.choices(string.ascii_lowercase, k=8))
elif not (resource_prefix.isalpha() and resource_prefix.islower()):
    raise NonRecoverableError("Provided resource prefix (%s) is invalid; must be all lowercase letters")

ctx.logger.info("Resource prefix to use: %s", resource_prefix)

availability_zone_1 = '{}{}'.format(aws_region, az1_suffix)
availability_zone_2 = '{}{}'.format(aws_region, az2_suffix)
network_deployment_id = '{}_network'.format(ctx.deployment.id)

configuration = {
    'current_deployment_id': ctx.deployment.id,
    'network': {
        'deployment_id': network_deployment_id,
        'inputs': {
            'app_deployment_id': ctx.deployment.id,
            'aws_region_name': aws_region,
            'resource_prefix': resource_prefix,
            'availability_zone_1': availability_zone_1,
            'availability_zone_2': availability_zone_2
        }
    },
    'k8s': {
        'inputs': {
            'network_deployment_id': network_deployment_id
        }
    },
    'db': {
        'inputs': {
            'network_deployment_id': network_deployment_id,
            'master_username': db_master_username,
            'master_password': db_master_password
        }
    },
    's3': {
        'inputs': {
            'bucket_name': '{}bucket'.format(resource_prefix),
            'bucket_region': aws_region
        }
    }
}

if env_type == 'dev':
    configuration['network']['inputs'].update({
        'ami_id': AWS_RESOURCES[aws_region]['ami'],
        'instance_type': 't2.medium'
    })
    configuration['s3']['inputs'].update({
        'network_deployment_id': network_deployment_id
    })
elif env_type == 'production':
    for component in ['k8s', 'db', 's3']:
        configuration[component]['inputs']['aws_region_name'] = aws_region
        if component != 's3':
            configuration[component]['inputs']['resource_prefix'] = resource_prefix

    configuration['k8s']['inputs'].update({
        'eks_cluster_name': '{}_eks_cluster'.format(resource_prefix),
        'eks_nodegroup_name': '{}_eks_nodegroup'.format(resource_prefix)
    })
    configuration['db']['inputs'].update({
        'stack_name': '{}-stack'.format(resource_prefix),
        'db_name': '{}rdspsql'.format(resource_prefix)
    })
else:
    raise Exception("Unhandled environment type: {}".format(env_type))

for component in ['network', 'k8s', 'db', 's3']:
    configuration[component]['blueprint'] = COMPONENT_BLUEPRINTS[component][env_type]

ctx.instance.runtime_properties.update(configuration)
