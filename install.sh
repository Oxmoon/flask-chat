#!/bin/bash
if docker volume ls | grep -q "flask-chat_db-data"; then
    read -p "This will erase all flask-chat db data. Are you sure?[Y/y] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker volume rm flask-chat_db-data
    fi
fi
source ./.env
cat <<EOF > init.sql
CREATE USER ${PRO_USER} WITH PASSWORD '${PRO_PASSWORD}';
CREATE USER ${DEV_USER} WITH PASSWORD '${DEV_PASSWORD}';
CREATE USER ${TEST_USER} WITH PASSWORD '${TEST_PASSWORD}';
CREATE DATABASE pro_db;
CREATE DATABASE dev_db;
CREATE DATABASE test_db;
GRANT ALL PRIVILEGES ON DATABASE pro_db TO ${PRO_USER};
GRANT ALL PRIVILEGES ON DATABASE dev_db TO ${DEV_USER};
GRANT ALL PRIVILEGES ON DATABASE test_db TO ${TEST_USER};
GRANT pg_read_all_data TO ${PRO_USER};
GRANT pg_write_all_data TO ${PRO_USER};
GRANT pg_read_all_data TO ${DEV_USER};
GRANT pg_write_all_data TO ${DEV_USER};
GRANT pg_read_all_data TO ${TEST_USER};
GRANT pg_write_all_data TO ${TEST_USER};
GRANT ALL PRIVILEGES ON DATABASE pro_db TO ${PRO_USER};
GRANT ALL PRIVILEGES ON DATABASE dev_db TO ${DEV_USER};
GRANT ALL PRIVILEGES ON DATABASE test_db TO ${TEST_USER};
\c pro_db postgres
GRANT ALL ON SCHEMA public TO ${PRO_USER};
\c dev_db postgres
GRANT ALL ON SCHEMA public TO ${DEV_USER};
\c test_db postgres
GRANT ALL ON SCHEMA public TO ${TEST_USER};
EOF
chmod +x ./init.sql
