# Environment-as-a-Service (EaaS): Development vs. Production Environments

This repository contains a demo of using Cloudify's Service Components feature, in order
to provide Environment-as-a-Service (EaaS) functionality based on the distinction between
development and production environments.

## Overview

This demo consists of:

* Infrastructure blueprints, describing how different infrastructure components are laid out.
* An application blueprint, describing the application.

## Application Blueprint

The application blueprint uses the Service Components feature to dynamically select the infrastructure
blueprints to use. The decision is performed during application installation time, based on a business-oriented
(rather than physical) input - `env_type` - with the possible value of `dev` or `production`.

The application blueprint is located in [app/blueprint.yaml](app/blueprint.yaml).

The blueprint requires the following inputs:

| Input | Description |
|-------|-------------|
| `vpc_deployment_id` | The deployment ID of the `vpc` blueprint to use for VPC information |
| `resource_prefix` | Prefix to attach to created resources' names |
| `env_type` | Type of environment from SDLC perspective. Must be either `dev` or `production` |
| `db_master_username` | Name of superuser account to create in the database |
| `db_master_password` | Password of database's superuser |

## Infrastructure Blueprints

| Blueprint | Category | Description
|-----------|----------|------------
| [`vpc`](infra/vpc/) | General | Creates a VPC with all prerequisites for the application
| [`minikube`](infra/dev/minikube/) | Compute | A Compute environment consisting of a Kubernetes cluster inside an AWS virtual machine
| `eks` | Compute | A Compute environment consisting of an Elastic Kubernetes cluster on AWS (see below)
| [`vm_with_psql`](infra/dev/vm_with_psql/) | Database | A PostgreSQL installation on a virtual machine
| [`rds_psql`](infra/prod/rds_psql/) | Database | An AWS RDS instance of PostgreSQL, created by AWS CloudFormation
| [`minio`](infra/dev/minio/) | File storage | S3-compatible file storage using `minio` on a virtual machine
| [`s3`](infra/prod/s3/) | File storage | An S3 bucket

*Note*: the EKS blueprint is not located here - you can find it in our [community repository](https://github.com/cloudify-community/blueprint-examples/tree/master/kubernetes/aws-eks).

## Using the Demo

1. Make sure that the required secrets are defined on Cloudify Manager, as follows:

   |Secret|Description|
   |------|-----------|
   | `aws_access_key_id` | AWS access key |
   | `aws_secret_access_key` | AWS secret key |
   | `aws_region_name` | (Optional) AWS region to use. If not configured, then the `aws_region_name` input must be provided to the application |
   | `aws_keypair` | Name of AWS keypair to associate virtual machines with |
   | `private_key_content` | The SSH private key (the actual contents) for the keypair specified by `aws_keypair` |

2. Upload all infrastructure blueprints described above. With the exception of the `vpc` blueprint,
   make sure to use the correct blueprint ID for each blueprint (the "Blueprint" column
   contains the blueprint ID).

3. Upload the application blueprint from [app/blueprint.yaml](app/blueprint.yaml). We will assume that its
   ID is `app`.
   
4. Create a deployment from the `vpc` blueprint, and note the deployment's ID (we will use `demo-vpc` in this document).

5. Install the `demo-vpc` deployment.

6. Create a "development" deployment of the `app` blueprint, and install it:

   ```bash
   cfy deployments create app_dev -b app -i env_type=dev -i vpc_deployment_id=demo-vpc -i resource_prefix=appdev -i db_master_username=psqladmin -i db_master_password=MyTestPa33w0rd!
   cfy executions start install -d app_dev
   ```

7. Create a "production" deployment of the `app` blueprint, and install it:

   ```bash
   cfy deployments create app_prod -b app -i env_type=production -i vpc_deployment_id=demo-vpc -i resource_prefix=appprod -i db_master_username=psqladmin -i db_master_password=MyTestPa33w0rd!
   cfy executions start install -d app_prod
   ```

At this point, both environments are up. Using the `cfy deployments capabilities` command, you can get the
capabilities of both environments.

```bash
$ cfy deployments capabilities app_dev
```

Output:

```
Retrieving capabilities for deployment app_dev...
 - "k8s_endpoint":
     Description: Kubernetes cluster's endpoint
     Value: https://52.55.81.150
 - "db_host":
     Description: Database's host
     Value: 54.236.168.125
 - "bucket_url":
     Description: URL of S3 bucket
     Value: http://34.232.15.134:9000/appdevbucket
```

```bash
$ cfy deployments capabilities app_prod
```

Output:

```
Retrieving capabilities for deployment app_prod...
 - "k8s_endpoint":
     Description: Kubernetes cluster's endpoint
     Value: https://BD12F68AE44744EAF129FBDE0BEBC9A9.yl4.us-east-1.eks.amazonaws.com
 - "db_host":
     Description: Database's host
     Value: am1ku2p1oyp6w7p.csfpro6oep8i.us-east-1.rds.amazonaws.com
 - "bucket_url":
     Description: URL of S3 bucket
     Value: https://s3.us-east-2.amazonaws.com/appprodbucket
```
