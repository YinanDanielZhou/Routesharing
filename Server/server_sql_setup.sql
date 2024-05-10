DROP DATABASE IF EXISTS server;
CREATE DATABASE server;
USE server;

CREATE TABLE CarSamples (
    car_id INTEGER NOT NULL,
    content TEXT NOT NULL
);

CREATE USER 'mytestuser'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON server.* TO 'mytestuser'@'%';
FLUSH PRIVILEGES;