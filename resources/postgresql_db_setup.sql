DROP DATABASE IF EXISTS locus_db;
DROP USER locus;
CREATE DATABASE locus_db;
CREATE USER locus WITH PASSWORD 'locus';
ALTER ROLE locus SET client_encoding TO 'utf8';
ALTER ROLE locus SET default_transaction_isolation TO 'read committed';
ALTER ROLE locus SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE locus_db TO locus;


