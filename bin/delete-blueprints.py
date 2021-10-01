#!/usr/bin/env python

import os
import subprocess
import threading


def perform(**kwargs):
    def _thread_body(blueprint_id):
        print("Deleting blueprint '{}' from the manager.".format(blueprint_id))
        subprocess.check_call(
            ['cfy', 'blueprints', 'delete', blueprint_id])

    script_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.normpath(os.path.join(script_dir, '..'))

    blueprints = ['nginx', 'eaas', 'vpc', 'rg']

    for env_type in ['dev', 'prod']:
        env_blueprints = os.listdir(os.path.join(root_dir, 'infra', env_type))
        for env_blueprint in env_blueprints:
            for file in os.listdir(os.path.join(root_dir, 'infra', env_type, env_blueprint)):
                if file.endswith("blueprint.yaml"):
                    if file.startswith("aws"):
                        blueprints.append("aws_{}".format(env_blueprint))
                    elif file.startswith("azure"):
                        blueprints.append("azure_{}".format(env_blueprint))
                    else:
                        blueprints.append(env_blueprint)

    threads = []
    for blueprint_id in blueprints:
        thread = threading.Thread(target=_thread_body, args=[blueprint_id])
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()


if __name__ == '__main__':
    perform()
