#!/bin/bash -e

sudo su - docker -c 'minikube start'
sleep 20
sudo su docker
minikube kubectl -- apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: demo-account
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: demo-account
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: demo-account-admin
subjects:
- kind: ServiceAccount
  name: demo-account
  namespace: default
EOF
minikube kubectl -- apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: demo-account-secret
  annotations:
    kubernetes.io/service-account.name: demo-account
type: kubernetes.io/service-account-token
EOF
export TOKEN=$(minikube kubectl -- get serviceaccount demo-account -o=jsonpath='{.secrets[0].name}' | xargs minikube kubectl -- get secret -ojsonpath='{.data.token}' | base64 --decode)
ctx instance runtime-properties token $TOKEN
