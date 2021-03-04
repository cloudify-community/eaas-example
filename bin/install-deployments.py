#!/usr/bin/env python

import os
import subprocess
import threading
import json
import tempfile
import time

from cloudify_cli.cli.cfy import pass_client
from cloudify_cli.constants import DEFAULT_TENANT_NAME

DEPLOYMENTS = {
    "aws_dev_small": {
        "tenant": DEFAULT_TENANT_NAME,
        "inputs": {
            "cloud_type": "aws",
            "env_type": "dev-small"
        }
    },
    "aws_dev_large": {
        "tenant": DEFAULT_TENANT_NAME,
        "inputs": {
            "cloud_type": "aws",
            "env_type": "dev-large"
        }
    },
    "aws_prod": {
        "tenant": DEFAULT_TENANT_NAME,
        "inputs": {
            "cloud_type": "aws",
            "env_type": "production"
        }
    },
    "az_dev_small": {
        "tenant": DEFAULT_TENANT_NAME,
        "inputs": {
            "cloud_type": "azure",
            "env_type": "dev-small"
        }
    },
    "az_dev_large": {
        "tenant": DEFAULT_TENANT_NAME,
        "inputs": {
            "cloud_type": "azure",
            "env_type": "dev-large"
        }
    },
    "az_prod": {
        "tenant": DEFAULT_TENANT_NAME,
        "inputs": {
            "cloud_type": "azure",
            "env_type": "production"
        }
    }
}

@pass_client()
def perform(client, **kwargs):
    def _thread_body(deployment_id, tenant_name, inputs):
        print("Creating deployment '{}' on tenant '{}' using inputs: {}".format(
            deployment_id, tenant_name, inputs))

        with tempfile.NamedTemporaryFile(suffix=".json", mode='w+', delete=False) as inputs_file:
            json.dump(inputs, inputs_file)
            inputs_file.close()
            subprocess.check_call(
                ['cfy', 'deployments', 'create', deployment_id, '-b', 'app', '-t', tenant_name, '-i', inputs_file.name])
            os.remove(inputs_file.name)

        time.sleep(5)
        print("Starting 'install' for deployment: {}".format(deployment_id))
        client._client._set_header('Tenant', tenant_name)
        client.executions.start(deployment_id, 'install')

    threads = []
    for deployment_id, dep_details in DEPLOYMENTS.items():
        tenant_name = dep_details['tenant']
        inputs = dep_details['inputs']
        thread = threading.Thread(target=_thread_body, args=(deployment_id, tenant_name, inputs))
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()


if __name__ == '__main__':
    perform()
