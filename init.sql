CREATE USER docker_pro WITH PASSWORD 'propassword';
CREATE USER docker_dev WITH PASSWORD 'devpassword';
CREATE USER docker_test WITH PASSWORD 'testpassword';
CREATE DATABASE pro_db;
CREATE DATABASE dev_db;
CREATE DATABASE test_db;
GRANT ALL PRIVILEGES ON DATABASE pro_db TO docker_pro;
GRANT ALL PRIVILEGES ON DATABASE dev_db TO docker_dev;
GRANT ALL PRIVILEGES ON DATABASE test_db TO docker_test;
GRANT pg_read_all_data TO docker_pro;
GRANT pg_write_all_data TO docker_pro;
GRANT pg_read_all_data TO docker_dev;
GRANT pg_write_all_data TO docker_dev;
GRANT pg_read_all_data TO docker_test;
GRANT pg_write_all_data TO docker_test;
GRANT ALL PRIVILEGES ON DATABASE pro_db TO docker_pro;
GRANT ALL PRIVILEGES ON DATABASE dev_db TO docker_dev;
GRANT ALL PRIVILEGES ON DATABASE test_db TO docker_test;
\c pro_db postgres
GRANT ALL ON SCHEMA public TO docker_pro;
\c dev_db postgres
GRANT ALL ON SCHEMA public TO docker_dev;
\c test_db postgres
GRANT ALL ON SCHEMA public TO docker_test;
