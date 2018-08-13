create database hernandb;
use hernandb;
create table tasks(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, title VARCHAR(50) NULL, description VARCHAR(500) NULL, done BOOLEAN);