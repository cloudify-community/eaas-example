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
| `env_type` | Type of environment from SDLC perspective; must be either `dev` or `production` |
| `resource_prefix` | Prefix to attach to created resources' names, must be lowercase characters only (default: randomly generated - see note below) |
| `aws_region_name` | Name of AWS region to operate on (default: `us-west-1`) |
| `db_master_username` | Name of superuser account to create in the database (default: `psqladmin`) |
| `db_master_password` | Password of database's superuser (default: randomly generated - see note below) |

**NOTES**:

* `db_master_password` and/or `resource_prefix` may be left out when creating a deployment, in which case
  they will be randomly generated. They can be obtained through the application deployment's
  capabilities, at the end of the installation.

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
   | `aws_keypair` | Name of AWS keypair to associate virtual machines with |
   | `private_key_content` | The SSH private key (the actual contents) for the keypair specified by `aws_keypair` |

2. Upload all infrastructure blueprints described above. Make sure to use the correct blueprint ID for
   each blueprint (the "Blueprint" column contains the blueprint ID).

   a. Note that the EKS blueprint should be uploaded from our community repository (see link above).

3. Upload the application blueprint from [app/blueprint.yaml](app/blueprint.yaml). We will assume that its
   ID is `app`.
   
4. Create a "development" deployment of the `app` blueprint, and install it:

   ```bash
   cfy deployments create app_dev -b app -i env_type=dev
   cfy executions start install -d app_dev
   ```

5. Create a "production" deployment of the `app` blueprint, and install it:

   ```bash
   cfy deployments create app_prod -b app -i env_type=production
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
     Value: https://50.18.139.105
 - "db_host":
     Description: Database's host
     Value: 184.72.34.182
 - "db_master_password":
     Description: Database's master password
     Value: uT36qtCx5WcSGeL4
 - "bucket_url":
     Description: URL of S3 bucket
     Value: http://54.219.29.17:9000/fiyxbvopbucket
```

```bash
$ cfy deployments capabilities app_prod
```

Output:

```
Retrieving capabilities for deployment app_prod...
 - "k8s_endpoint":
     Description: Kubernetes cluster's endpoint
     Value: https://336EA5CFF709771B2C76A58B7E750E20.yl4.us-west-1.eks.amazonaws.com
 - "db_host":
     Description: Database's host
     Value: gmubhvwbwbvmr2.c3lp69snztk6.us-west-1.rds.amazonaws.com
 - "db_master_password":
     Description: Database's master password
     Value: dm6C9ick0lHmsf8s
 - "bucket_url":
     Description: URL of S3 bucket
     Value: https://s3.us-west-1.amazonaws.com/gzscjpgibucket
```
