#!/bin/bash -e

bucket_name=$(ctx node properties bucket_name)
bucket_region=$(ctx node properties bucket_region)

mc mb --region ${bucket_region} local/${bucket_name}
