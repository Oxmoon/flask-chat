CREATE USER docker WITH PASSWORD 'password';
CREATE DATABASE pro_db;
GRANT ALL PRIVILEGES ON DATABASE pro_db TO docker;
GRANT ALL PRIVILEGES ON DATABASE dev_db TO docker;
GRANT ALL PRIVILEGES ON DATABASE test_db TO docker;
GRANT pg_read_all_data TO docker;
GRANT pg_write_all_data TO docker;

GRANT ALL PRIVILEGES ON DATABASE pro_db TO docker;
GRANT ALL PRIVILEGES ON DATABASE dev_db TO docker;
GRANT ALL PRIVILEGES ON DATABASE test_db TO docker;
\c pro_db postgres
GRANT ALL ON SCHEMA public TO docker;
\c dev_db postgres
GRANT ALL ON SCHEMA public TO docker;
\c test_db postgres
GRANT ALL ON SCHEMA public TO docker;
