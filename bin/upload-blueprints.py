#!/usr/bin/env python

import os
import subprocess
import threading


def perform(**kwargs):
    def _thread_body(blueprint_id, blueprint_path):
        print("Uploading blueprint '{}' from {}".format(blueprint_id,
                                                        blueprint_path))
        subprocess.check_call(
            ['cfy', 'blueprints', 'upload', blueprint_path, '-b', blueprint_id, '--visibility', 'global'])

    def _create_blueprint_tuple(file, env_blueprint, root_dir, env_type, cloud_type=None):
        if "standalone" in file and cloud_type:
            return ("{}_standalone_{}".format(cloud_type, env_blueprint),
                    os.path.join(root_dir,
                                 'infra',
                                 env_type,
                                 env_blueprint,
                                 file))
        elif "standalone" not in file and cloud_type:
            return ("{}_{}".format(cloud_type, env_blueprint),
                    os.path.join(root_dir,
                                 'infra',
                                 env_type,
                                 env_blueprint,
                                 file))
        elif "standalone" in file and not cloud_type:
            return ("standalone_{}".format(env_blueprint),
                    os.path.join(root_dir,
                                 'infra',
                                 env_type,
                                 env_blueprint,
                                 file))
        else:
            return (env_blueprint,
                    os.path.join(root_dir,
                                 'infra',
                                 env_type,
                                 env_blueprint,
                                 file))

    script_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.normpath(os.path.join(script_dir, '..'))

    blueprints = [
        ('nginx', os.path.join(root_dir, 'services/nginx.yaml')),
        ('aws', os.path.join(root_dir, 'environments/aws.yaml')),
        ('azure', os.path.join(root_dir, 'environments/azure.yaml')),
        ('eaas', os.path.join(root_dir, 'environments/eaas.yaml')),
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
                        blueprints.append(_create_blueprint_tuple(file, env_blueprint, root_dir, env_type, "aws"))
                    elif file.startswith("azure"):
                        blueprints.append(_create_blueprint_tuple(file, env_blueprint, root_dir, env_type, "azure"))
                    else:
                        blueprints.append(_create_blueprint_tuple(file, env_blueprint, root_dir, env_type))

    threads = []
    for blueprint_id, blueprint_path in blueprints:
        thread = threading.Thread(target=_thread_body, args=(blueprint_id, os.path.join(root_dir, blueprint_path)))
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()


if __name__ == '__main__':
    perform()
