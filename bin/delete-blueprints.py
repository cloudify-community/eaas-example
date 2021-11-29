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

    def _create_blueprint_name(file, env_blueprint, cloud_type=None):
        if "standalone" in file and cloud_type:
            return "{}_standalone_{}".format(cloud_type, env_blueprint)
        elif "standalone" not in file and cloud_type:
            return "{}_{}".format(cloud_type, env_blueprint)
        elif "standalone" in file and not cloud_type:
            return "standalone_{}".format(env_blueprint)
        else:
            return env_blueprint

    blueprints = ['nginx', 'eaas', 'vpc', 'rg', 'aws', 'azure']

    for env_type in ['dev', 'prod']:
        env_blueprints = os.listdir(os.path.join(root_dir, 'infra', env_type))
        for env_blueprint in env_blueprints:
            for file in os.listdir(os.path.join(root_dir, 'infra', env_type, env_blueprint)):
                if file.endswith("blueprint.yaml"):
                    if file.startswith("aws"):
                        blueprints.append(_create_blueprint_name(file, env_blueprint, "aws"))
                    elif file.startswith("azure"):
                        blueprints.append(_create_blueprint_name(file, env_blueprint, "azure"))
                    else:
                        blueprints.append(_create_blueprint_name(file, env_blueprint))

    threads = []
    for blueprint_id in blueprints:
        thread = threading.Thread(target=_thread_body, args=[blueprint_id])
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()


if __name__ == '__main__':
    perform()
