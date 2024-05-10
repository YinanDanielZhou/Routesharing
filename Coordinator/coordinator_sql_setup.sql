DROP DATABASE IF EXISTS coordinator;
CREATE DATABASE coordinator;
USE coordinator;

CREATE TABLE Consumers (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    compensation REAL NOT NULL,
    frequency REAL NOT NULL
);

CREATE TABLE Servers (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(45) NOT NULL,
    port INTEGER NOT NULL,
    UNIQUE KEY unique_machine (ip, port)
);

CREATE TABLE ConsumerUsingServer (
    consumer_id INTEGER NOT NULL,
    server_id INTEGER NOT NULL,
    PRIMARY KEY (consumer_id, server_id),
    FOREIGN KEY(consumer_id) REFERENCES Consumers(id),
    FOREIGN KEY(server_id) REFERENCES Servers(id)
);

CREATE TABLE CarSupplyConsumer (
    car_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    consumer_id INTEGER NOT NULL,
    payment_method TEXT NOT NULL,
    FOREIGN KEY(consumer_id) REFERENCES Consumers(id)
);

CREATE USER 'mytestuser'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON coordinator.* TO 'mytestuser'@'%';
FLUSH PRIVILEGES;