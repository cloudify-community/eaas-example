#!/usr/bin/env python

from cloudify import ctx
import os
import yaml


kubeconfig_path = '/home/docker/.kube/config'
kubeconfig_raw = os.popen('sudo cat ' + kubeconfig_path)
kube_config_dict = yaml.safe_load(kubeconfig_raw.read())
# ctx.instance.runtime_properties['config'] = kube_config_dict

ca_path = '/home/docker/.minikube/ca.crt'
ca_raw = os.popen('sudo cat ' + ca_path)
crt_path = '/home/docker/.minikube/profiles/minikube/client.crt'
crt_raw = os.popen('sudo cat ' + crt_path)
key_path = '/home/docker/.minikube/profiles/minikube/client.key'
key_raw = os.popen('sudo cat ' + key_path)

kube_config_dict['clusters'][0]['cluster']['certificate-authority'] = \
    ca_raw.read()
kube_config_dict['clusters'][0]['cluster']['server'] = \
    'https://' + str(HOST_VM_IP) + ':8443'
kube_config_dict['users'][0]['user']['client-certificate'] = \
    crt_raw.read()
kube_config_dict['users'][0]['user']['client-key'] = \
    key_raw.read()

ctx.instance.runtime_properties['config'] = kube_config_dict
