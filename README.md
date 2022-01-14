# Environment-as-a-Service (EaaS): Development vs. Production Environments

This repository contains a demo of using Cloudify's Service Components feature, in order
to provide Environment-as-a-Service (EaaS) functionality based on the distinction between
development and production environments.

A webinar slide deck is also available [here](https://docs.google.com/presentation/d/1N70lyLPnw7CXp00X5CSSS3hSfTpWgj5HzQOB-ZE_0P4).

## Overview

This demo consists of:

* Infrastructure blueprints, describing how different infrastructure components are laid out.
* An EAAS blueprint, describing the Environment as a Service scenario.
* Parent blueprints (aws & azure), describing how to pass constant inputs such as credentials to the EaaS subenvironments.

## Parent Blueprints (AWS, Azure)

The parent blueprints are exposing some of the secret values depending on the cloud type (AWS, Azure), which later are leveraged
by EAAS blueprint to deploy the Environment as a Service scenario using the Environments Capabilities. They just have to be
installed in your Cloudify Manager tenant, so you can use them.

The only input is the `region_name`, which you have to set. Default examples are using `us-west-1` in AWS & `westus` location in Azure.

## EAAS Blueprint

The EAAS blueprint uses the Service Components and Environment Capabilities to dynamically select the infrastructure
blueprints to use. The decision is performed during EAAS installation time, based on a business-oriented
(rather than physical) inputs:
* `env_type` - with the possible value of `dev` or `production`
and labels:
* `csys-obj-parent` - which is being set automatically when "Deploy on" is being used.

Depending on the value of `env_type`, the following will be set up:

| `env_type`   | Compute | Database | File Storage | Comments
|--------------|---------|----------|--------------|-----------------
| `dev_small`  | Minikube | PostgreSQL | Minio | All components in a single VM
| `dev_large`  | Minikube | PostgreSQL | Minio | Each component in its own VM
| `production` | EKS/AKS  | PostgreSQL on RDS | S3 |

The EaaS blueprint is located in [environments/eaas.yaml](environments/eaas.yaml).

The blueprint requires the following inputs:

| Input | Description |
|-------|-------------|
| `env_type` | Type of environment from SDLC perspective; must be either `dev-small`, `dev-large` or `production` |
| `resource_prefix` | Prefix to attach to created resources' names, must be lowercase characters only (default: randomly generated - see note below) |

And the following labels:

| Label | Description |
|-------|-------------|
| `csys-obj-parent` | Parent deployment which provides constant values for some cloud-specific inputs, must be either `aws` or `azure` (can be set automatically when using `Deploy On` button) |
| `csys-obj-type` | Must be set to `environment` (it is being set automatically) |

**NOTES**:

* `resource_prefix` may be left out when creating a deployment, in which case
  it will be randomly generated.

## Infrastructure Blueprints

| Blueprint | Category | Description
|-----------|----------|------------
| [`vpc`](infra/vpc) | General | Creates a VPC with all prerequisites for the application (see note below)
| [`rg`](infra/rg) | General | Creates a RG (Resource Group) with all prerequisites for the application (see note below)
| [`vm`](infra/dev/vm) | General | Creates a VM with an elastic IP
| [`single_node`](infra/dev/single_node) | Network | Creates a simple network inside the VPC/RG, and a VM to host other components in
| [`multi_node`](infra/dev/multi_node) | Network | Creates a simple network inside the VPC/RG, and three VM's to host other components in
| [`prod_network`](infra/prod/prod_network) | Network | Creates a complex network inside the VPC/RG, to accommodate for EKS/AKS
| [`minikube`](infra/dev/minikube) | Compute | A Compute environment consisting of a Kubernetes cluster inside a VM
| [`eks`](infra/prod/eks) | Compute | A Compute environment consisting of an Elastic Kubernetes cluster on AWS
| [`aks`](infra/prod/aks) | Compute | A Compute environment consisting of an Azure Kubernetes cluster on Azure
| [`psql`](infra/dev/psql) | Database | A PostgreSQL installation on a VM
| [`rds_psql`](infra/prod/rds_psql) | Database | An RDS instance of PostgreSQL, created by AWS CloudFormation/Azure ARM
| [`minio`](infra/dev/minio) | File storage | S3-compatible file storage using `minio` on a VM
| [`s3`](infra/prod/s3) | File storage | An S3 bucket/blob created by Terraform
| [`sqs`](infra/prod/sqs) | Queue service | An SQS service created by AWS plugin (AWS only)

**NOTES**

* The `vpc` blueprint creates a VPC using Cloudify's AWS plugin. There also exists a blueprint
  under [`vpc-tf`](infra/vpc-tf), which does the same using Terraform. If you're interested to work
  with the Terraform variant, just upload the blueprint in [infra/vpc-tf](infra/vpc-tf) using the
  blueprint ID `vpc`.
* Moreover, `rg` blueprint also has its Terraform variant.

## Using the Demo

1. Make sure that the required secrets are defined on Cloudify Manager, as follows:

   |Secret|Description|
   |------|-----------|
   | `aws_access_key_id` | AWS access key |
   | `aws_secret_access_key` | AWS secret key |
   | `aws_keypair` | Name of AWS keypair to associate virtual machines with |
   | `azure_tenant_id` | Azure tenant ID |
   | `azure_subscription_id` | Azure subscription ID |
   | `azure_client_id` | Azure client ID |
   | `azure_client_secret` | Azure client secret |
   | `public_key_content` | The SSH public key (the actual contents) for the keypair specified by `aws_keypair` |
   | `private_key_content` | The SSH private key (the actual contents) for the keypair specified by `aws_keypair` |
   | `eaas_params` | Some constant secret values like AMI IDs or default passwords. You can use [secret.json](secret.json) to import this secret |

2. Upload the required plugins to Cloudify Manager:

   * AWS plugin (version 2.5.6+)
   * Azure plugin (version 3.0.10+)
   * Kubernetes plugin (version 2.9.3+)
   * Terraform plugin (version 0.15.0+)
   * Fabric plugin (version 2.0.7+)

3. Download this repository as a `tar.gz` or `zip` file (Using the `Code` button on Github), and extract
   it to your file system.

4. Upload all infrastructure blueprints described above. Make sure to use the correct blueprint ID for
   each blueprint (the "Blueprint" column contains the blueprint ID; 
   feel free to use [bin/upload-blueprints.py](bin/upload-blueprints.py)).

5. Upload the application blueprint from [environments/eaas.yaml](environments/eaas.yaml). We will assume that its
   ID is `eaas`.

6. Install parent deployments, which are located in [environments/aws.yaml](environments/aws.yaml) and [environments/azure.yaml](environments/azure.yaml)
   You don't have to install both environments, if you want to work e.g. only with AWS. Feel free to choose.
    
    ```bash
   cfy deployments create aws -b aws -i aws_region_name=us-west-1
   cfy deployments create azure -b azure -i azure_location_name=westus
   
   cfy executions start install -d aws
   cfy executions start install -d azure
   ```
   
7. Create a "development-small" deployment of the `eaas` blueprint, and install it e.g. on AWS:

   ```bash
   cfy deployments create eaas_dev_small -b eaas  -i env_type=dev-small --labels csys-obj-parent=aws
   cfy executions start install -d eaas_dev_small
   ```

8. Create a "development-large" deployment of the `eaas` blueprint, and install it on Azure:

   ```bash
   cfy deployments create eaas_dev_large -b eaas  -i env_type=dev-large --labels csys-obj-parent=azure
   cfy executions start install -d eaas_dev_large
   ```

9. Create a "production" deployment of the `eaas` blueprint, and install it on AWS:

   ```bash
   cfy deployments create eaas_prod -b app -i env_type=production --labels csys-obj-parent=aws
   cfy executions start install -d eaas_prod
   ```

At this point, both environments are up. Using the `cfy deployments capabilities` command, you can get the
capabilities of both environments.

```bash
$ cfy deployments capabilities eaas_dev_small
```

Output:

```
Retrieving capabilities for deployment eaas_dev_small...
 - "k8s_endpoint":
     Description: Kubernetes cluster's endpoint
     Value: https://54.215.37.150
 - "k8s_config":
     Description: Kubernetes cluster's config
     Value: {...}
 - "db_host":
     Description: Database's host
     Value: 54.215.37.150
 - "db_master_username":
     Description: Database's master username
     Value: psqladmin
 - "db_master_password":
     Description: Database's master password
     Value: 10XaGXdTS7q6tccU
 - "bucket_url":
     Description: URL of S3 bucket
     Value: http://54.215.37.150:9000/uawbkxvcbucket
```

```bash
$ cfy deployments capabilities eaas_dev_large
```

Output:

```
Retrieving capabilities for deployment eaas_dev_large...
 - "k8s_endpoint":
     Description: Kubernetes cluster's endpoint
     Value: https://gbmqeavraks-9361aa37.hcp.westus.azmk8s.io:443
 - "k8s_config":
     Description: Kubernetes cluster's config
     Value: {...}
 - "db_host":
     Description: Database's host
     Value: gbmqeavr-postgresql-server.postgres.database.azure.com
 - "db_master_username":
     Description: Database's master username
     Value: psqladmin
 - "db_master_password":
     Description: Database's master password
     Value: udY71PO43qdLUCa4
 - "bucket_url":
     Description: URL of S3 bucket
     Value: https://gbmqeavrblob.blob.core.windows.net/gbmqeavrblob-container
```

```bash
$ cfy deployments capabilities eaas_prod
```

Output:

```
Retrieving capabilities for deployment app_prod...
 - "k8s_endpoint":
     Description: Kubernetes cluster's endpoint
     Value: https://BA4A97B47496A0957695A5DCD2B58789.yl4.us-west-1.eks.amazonaws.com
 - "k8s_config":
     Description: Kubernetes cluster's config
     Value: {...}
 - "db_host":
     Description: Database's host
     Value: wms7oy7i1fp9hj.c3lp69snztk6.us-west-1.rds.amazonaws.com
 - "db_master_username":
     Description: Database's master username
     Value: psqladmin
 - "db_master_password":
     Description: Database's master password
     Value: 5IHk7ptPiFKvp1o9
 - "bucket_url":
     Description: URL of S3 bucket
     Value: https://wtgjexngbucket.s3.us-west-1.amazonaws.com
```

## GitActions configuration

There is an example GitHub Actions workflow defined for this repository, which can be used for updating the existing EaaS deployment directly from Git. The flow is the following: when there is a commit pushed to the branch, which name starts with "develop/", it uploads the latest eaas.yaml to the Cloudify Manager specified in repository secrets and installs a new deployment (if it doesn't exist yet) or triggers a deployment update using the latest blueprint. At the moment,  only production use case is supported. 

Cloudify GitHub Actions are being used here: https://github.com/marketplace?type=actions&query=cloudify

To connect the repository with a Cloudify Manager running EaaS example, the user has to set the following secrets (according to https://docs.cloudify.co/5.1/working_with/integration/#specifying-cloudify-manager-access):
* CLOUDIFY_HOST: Host name / IP address of Cloudify Manager
* CLOUDIFY_USERNAME: Username for Cloudify authentication
* CLOUDIFY_PASSWORD: Password for Cloudify authentication
* CLOUDIFY_TENANT: Cloudify tenant to operate on 
* CLOUDIFY_SSL: if it's non-ssl manager it can be set to "false", but if ssl is being used, the content of the SSL certificate should be placed here
* CLOUDIFY_SSL_TRUST_ALL: should be "true" in order to bypass certificate verification
