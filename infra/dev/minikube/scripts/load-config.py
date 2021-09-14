#!/usr/bin/env python

from cloudify import ctx
import os
import yaml


kubeconfig_path = '/home/docker/.kube/config'
kubeconfig_raw = os.popen('sudo cat ' + kubeconfig_path)
kube_config_dict = yaml.safe_load(kubeconfig_raw.read())

ca_path = '/home/docker/.minikube/ca.crt'
ca_raw = os.popen('sudo cat ' + ca_path)
crt_path = '/home/docker/.minikube/profiles/minikube/client.crt'
crt_raw = os.popen('sudo cat ' + crt_path)
key_path = '/home/docker/.minikube/profiles/minikube/client.key'
key_raw = os.popen('sudo cat ' + key_path)

kube_config_dict['clusters'][0]['cluster']['certificate-authority-data'] = \
    ca_raw.read()
kube_config_dict['clusters'][0]['cluster']['server'] = \
    'https://' + os.getenv('HOST_VM_IP')  + ':8443'
kube_config_dict['users'][0]['user']['client-certificate-data'] = \
    crt_raw.read()
kube_config_dict['users'][0]['user']['client-key-data'] = \
    key_raw.read()
del(kube_config_dict['clusters'][0]['cluster']['certificate-authority'])
del(kube_config_dict['users'][0]['user']['client-certificate'])
del(kube_config_dict['users'][0]['user']['client-key'])

ctx.instance.runtime_properties['config'] = kube_config_dict
