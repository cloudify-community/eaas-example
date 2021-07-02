#!/bin/bash -e

# Creating postgres backup
sudo su postgres -c "cd && pg_dumpall > /tmp/pg9backup"

# Installing new postgresql version
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
sudo yum install -y postgresql$POSTGRES_NEW_VERSION-server

# Migrating the database
sudo systemctl stop postgresql.service && sudo systemctl stop postgresql-$POSTGRES_NEW_VERSION.service
sudo su postgres -c "cd && /usr/pgsql-$POSTGRES_NEW_VERSION/bin/initdb -D /var/lib/pgsql/$POSTGRES_NEW_VERSION/data/"

sudo mv /usr/bin/pg_ctl{,-orig}
echo '#!/bin/bash' | sudo tee /usr/bin/pg_ctl
echo '"$0"-orig "${@/unix_socket_directory/unix_socket_directories}"' | sudo tee -a /usr/bin/pg_ctl
sudo chmod +x /usr/bin/pg_ctl

sudo su postgres -c "cd && /usr/pgsql-$POSTGRES_NEW_VERSION/bin/pg_upgrade --old-datadir /var/lib/pgsql/data/ --new-datadir /var/lib/pgsql/$POSTGRES_NEW_VERSION/data/ --old-bindir /usr/bin/ --new-bindir /usr/pgsql-$POSTGRES_NEW_VERSION/bin/"

sudo mv -f /usr/bin/pg_ctl{-orig,}

sudo cp /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/$POSTGRES_NEW_VERSION/data/
sudo cp /var/lib/pgsql/data/postgresql.conf /var/lib/pgsql/$POSTGRES_NEW_VERSION/data/

sudo systemctl start postgresql-$POSTGRES_NEW_VERSION.service
sudo systemctl enable postgresql-$POSTGRES_NEW_VERSION

# Restoring information from the old database
sudo su postgres -c "cd && psql -d postgres -f /tmp/pg9backup"
