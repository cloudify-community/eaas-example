#!/bin/bash -e

sudo yum install awscli -y

aws configure set aws_access_key_id ${aws_access_key_id}
aws configure set aws_secret_access_key ${aws_secret_access_key}
aws configure set default.region ${aws_region}

aws rds modify-db-instance \
    --db-instance-identifier ${db_instance_identifier} \
    --db-instance-class "${new_instance_class}" \
    --apply-immediately
