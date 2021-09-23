# Environment-as-a-Service (EaaS): Development vs. Production Environments

This repository contains a demo of using Cloudify's Service Components feature, in order
to provide Environment-as-a-Service (EaaS) functionality based on the distinction between
development and production environments.

A webinar slide deck is also available [here](https://docs.google.com/presentation/d/1N70lyLPnw7CXp00X5CSSS3hSfTpWgj5HzQOB-ZE_0P4).

## Overview

This demo consists of:

* Infrastructure blueprints, describing how different infrastructure components are laid out.
* An application blueprint, describing the application.

## Application Blueprint

The application blueprint uses the Service Components feature to dynamically select the infrastructure
blueprints to use. The decision is performed during application installation time, based on a business-oriented
(rather than physical) inputs:
* `env_type` - with the possible value of `dev` or `production`,
* `cloud_type` - with the possible value of `aws` or `azure`.

Depending on the value of `env_type`, the following will be set up:

| `env_type`   | Compute | Database | File Storage | Comments
|--------------|---------|----------|--------------|-----------------
| `dev_small`  | Minikube | PostgreSQL | Minio | All components in a single VM
| `dev_large`  | Minikube | PostgreSQL | Minio | Each component in its own VM
| `production` | EKS/AKS  | PostgreSQL on RDS | S3 |

The application blueprint is located in [app/blueprint.yaml](app/blueprint.yaml).

The blueprint requires the following inputs:

| Input | Description |
|-------|-------------|
| `env_type` | Type of environment from SDLC perspective; must be either `dev-small`, `dev-large` or `production` |
| `cloud_type` | Type of environment from cloud provider perspective; must be either `aws` or `azure` |
| `resource_prefix` | Prefix to attach to created resources' names, must be lowercase characters only (default: randomly generated - see note below) |
| `aws_region_name` | Name of AWS region to operate on (default: `us-west-1`) |
| `azure_location_name` | Name of Azure location to operate on (default: `westus`) |
| `db_master_username` | Name of superuser account to create in the database (default: `psqladmin`) |

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
   | `azure_tenant_id` | Azure tenant ID |
   | `azure_subscription_id` | Azure subscription ID |
   | `azure_client_id` | Azure client ID |
   | `azure_client_secret` | Azure client secret |
   | `aws_keypair` | Name of AWS keypair to associate virtual machines with |
   | `public_key_content` | The SSH public key (the actual contents) for the keypair specified by `aws_keypair` |
   | `private_key_content` | The SSH private key (the actual contents) for the keypair specified by `aws_keypair` |

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

5. Upload the application blueprint from [app/blueprint.yaml](app/blueprint.yaml). We will assume that its
   ID is `app`.
   
6. Create a "development-small" deployment of the `app` blueprint, and install it on AWS:

   ```bash
   cfy deployments create app_dev_small -b app -i env_type=dev-small -i cloud_type=aws
   cfy executions start install -d app_dev_small
   ```

7. Create a "development-large" deployment of the `app` blueprint, and install it on Azure:

   ```bash
   cfy deployments create app_dev_large -b app -i env_type=dev-large -i cloud_type=azure
   cfy executions start install -d app_dev_large
   ```

8. Create a "production" deployment of the `app` blueprint, and install it on AWS:

   ```bash
   cfy deployments create app_prod -b app -i env_type=production -i cloud_type=aws
   cfy executions start install -d app_prod
   ```

At this point, both environments are up. Using the `cfy deployments capabilities` command, you can get the
capabilities of both environments.

```bash
$ cfy deployments capabilities app_dev_small
```

Output:

```
Retrieving capabilities for deployment app_dev_small...
 - "k8s_endpoint":
     Description: Kubernetes cluster's endpoint
     Value: https://54.215.37.150
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
$ cfy deployments capabilities app_dev_large
```

Output:

```
Retrieving capabilities for deployment app_dev_large...
 - "k8s_endpoint":
     Description: Kubernetes cluster's endpoint
     Value: https://gbmqeavraks-9361aa37.hcp.westus.azmk8s.io:443
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
$ cfy deployments capabilities app_prod
```

Output:

```
Retrieving capabilities for deployment app_prod...
 - "k8s_endpoint":
     Description: Kubernetes cluster's endpoint
     Value: https://BA4A97B47496A0957695A5DCD2B58789.yl4.us-west-1.eks.amazonaws.com
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

## PostgreSQL version upgrade on AWS

### Development environments
To perform the PostgreSQL version upgrade on `dev` environment run `execute_operation` on:
- `aws-dev-small-vm` deployment when using "development-small" type
- `aws-dev-large-vm-db` deployment when using "development-large" type

Workflow parameters:
```
{
   "operation":"cloudify.interfaces.lifecycle.upgrade",
   "operation_kwargs":{
        "process": {
            "env": {
                "POSTGRES_NEW_VERSION": "10"
            }
        }
   },
   "allow_kwargs_override":true,
   "run_by_dependency_order":false,
   "type_names":[],
   "node_ids":[
      "upgrade_psql"
   ],
   "node_instance_ids":[]
}
```
`POSTGRES_NEW_VERSION` is the desired major version of PostgreSQL server.  
Should be provided as a string and have one of the following values: `10`, `11`, `12` or `13`.
Check with the `sudo systemctl -a | grep postgres` command if the desired version of PostgreSQL server is running.

### Production environment
To perform the PostgreSQL version upgrade on `prod` environment run `execute operation` on `aws-prod-database` deployment.  
Workflow parameters:
```
{
   "operation":"cloudify.interfaces.lifecycle.upgrade",
   "operation_kwargs":{
      "new_postgres_version": "12.7"
   },
   "allow_kwargs_override":true,
   "run_by_dependency_order":false,
   "type_names":[],
   "node_ids":[
      "upgrade_rds_psql_version"
   ],
   "node_instance_ids":[]
}
```
`new_postgres_version` parameter is the desired major version of PostgreSQL server to be run by AWS RDS.  
The solution uses AWS CLI which is installed on the Cloudify Manager VM and connects to user's AWS account using AWS access key and AWS secret access key stored in the secrets.  
The workflow automatically creates a snapshot of the RDS (backs-up database) and performs the upgrade
of PostgreSQL engine version if such an upgrade if possible.  
For information regarding AWS' requirements of PostgreSQL version upgrade, please refer to the 
[AWS documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.PostgreSQL.html).  

## PostgreSQL database manual scale on AWS

### Development environments
To perform the PostgreSQL database VM scale-up on `dev` environment run `Cloudify custom workflow` `scale vm` on:
- `aws-dev-small-vm` deployment when using "development-small" type
- `aws-dev-large-vm-db` deployment when using "development-large" type

The workflow takes the desired new instance type name from the `eaas_params` secret according to used environment type:
```
{
  "aws": {
    "dev-small": {
      "network": {
        "vm_scale_instance_name": "t2.large"
      }
    },
    "dev-large": {
      "network": {
        "vm_scale_instance_name": "t2.large"
      }
    }
  }
}
```
The virtual machine is stopped, modified and reconfigured to different instance type (scale-up) and then immediately started again.
To change the desired instance type after scale-up update the `eaas_params` secret in the Cloudify Manager's secrets store.

### Production environment
To perform the PostgreSQL database on RDS scale-up on `prod` environment run `execute operation` on `aws-prod-database` deployment.
```
{
   "operation":"cloudify.interfaces.lifecycle.upgrade",
   "operation_kwargs":{
      "new_instance_class": "db.t2.large"
   },
   "allow_kwargs_override":true,
   "run_by_dependency_order":false,
   "type_names":[],
   "node_ids":[
      "scale_up_rds"
   ],
   "node_instance_ids":[]
}
```
By default, the RDS is created and provisioned using DB instance class `db.t2.small`.  
`new_instance_class` parameter is the new desired DB instance class of the RDS instance.  
The solution uses AWS CLI which is installed on the Cloudify Manager VM and connects to user's AWS account using AWS access key and AWS secret access key stored in the secrets.  
For information regarding allowed RDS instance classes, please refer to the
[AWS documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html).  
