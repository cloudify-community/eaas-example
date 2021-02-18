#!/usr/bin/env python

import os
import subprocess
import threading


def perform(**kwargs):
    def _thread_body(blueprint_id, blueprint_path):
        print("Uploading blueprint '{}' from {}".format(blueprint_id,
                                                        blueprint_path))
        subprocess.check_call(
            ['cfy', 'blueprints', 'upload', blueprint_path, '-b', blueprint_id])

    script_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.normpath(os.path.join(script_dir, '..'))

    blueprints = [
        ('app', os.path.join(root_dir, 'app/blueprint.yaml')),
        ('vpc', os.path.join(root_dir, 'infra/vpc/blueprint.yaml')),
        ('rg', os.path.join(root_dir, 'infra/rg/blueprint.yaml'))
    ]
    for env_type in ['dev', 'prod']:
        env_blueprints = os.listdir(os.path.join(root_dir, 'infra', env_type))
        for env_blueprint in env_blueprints:
            for file in os.listdir(
                os.path.join(root_dir, 'infra', env_type, env_blueprint)
            ):
                if file.endswith("blueprint.yaml"):
                    if file.startswith("aws"):
                        blueprints.append(("aws_{}".format(env_blueprint),
                                           os.path.join(root_dir,
                                                        'infra',
                                                        env_type,
                                                        env_blueprint,
                                                        'aws-blueprint.yaml')))
                    elif file.startswith("azure"):
                        blueprints.append(("azure_{}".format(env_blueprint),
                                           os.path.join(root_dir,
                                                        'infra',
                                                        env_type,
                                                        env_blueprint,
                                                        'azure-blueprint.yaml'))
                        )
                    else:
                        blueprints.append((
                            env_blueprint,
                            os.path.join(root_dir,
                                         'infra',
                                         env_type,
                                         env_blueprint,
                                         'blueprint.yaml'))
                        )

    threads = []
    for blueprint_id, blueprint_path in blueprints:
        thread = threading.Thread(target=_thread_body, args=(blueprint_id, os.path.join(root_dir, blueprint_path)))
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()


if __name__ == '__main__':
    perform()
