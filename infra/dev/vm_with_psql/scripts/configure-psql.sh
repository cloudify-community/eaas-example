#!/bin/bash -e

temp_pw_file=$(mktemp)
echo ${master_password} > ${temp_pw_file}

export PGSETUP_INITDB_OPTIONS="-U ${master_username} --pwfile ${temp_pw_file}"
sudo postgresql-setup initdb
rm -f ${temp_pw_file}

ctx instance runtime-properties master_username ${master_username}
ctx instance runtime-properties master_password ${master_password}
