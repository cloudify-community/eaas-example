#!/usr/bin/env python

import os
import subprocess
import threading


def perform(**kwargs):
    def _thread_body(blueprint_id, blueprint_path):
        print("Uploading blueprint '{}' from {}".format(blueprint_id, blueprint_path))
        subprocess.check_call(
            ['cfy', 'blueprints', 'upload', blueprint_path, '-b', blueprint_id, '--visibility', 'global'])

    script_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.normpath(os.path.join(script_dir, '..'))

    blueprints = [
        ('app', os.path.join(root_dir, 'app/blueprint.yaml')),
        ('vpc', os.path.join(root_dir, 'infra/vpc/blueprint.yaml')),
    ]
    for env_type in ['dev', 'prod']:
        env_blueprints = os.listdir(os.path.join(root_dir, 'infra', env_type))
        for env_blueprint in env_blueprints:
            blueprints.append((env_blueprint, os.path.join(root_dir, 'infra', env_type, env_blueprint, 'blueprint.yaml')))

    threads = []
    for blueprint_id, blueprint_path in blueprints:
        thread = threading.Thread(target=_thread_body, args=(blueprint_id, os.path.join(root_dir, blueprint_path)))
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()


if __name__ == '__main__':
    perform()
