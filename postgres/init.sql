-- Initialize Echo database
CREATE DATABASE echo;
CREATE USER echo_user WITH PASSWORD 'echo_password';
GRANT ALL PRIVILEGES ON DATABASE echo TO echo_user;