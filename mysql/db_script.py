#!/usr/bin/env python3
import pymysql as mysql


def create_db():
    conn = mysql.connect("localhost", "root", "ATLanta1904")
    cursor = conn.cursor()
    cursor.execute('create database IF NOT EXISTS prueba')
    cursor.execute('create table IF NOT EXISTS prueba.tasks (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, ' +
                   'title VARCHAR(50) NULL, ' +
                   'description VARCHAR(500) NULL, ' +
                   'done BOOLEAN)')


if __name__ == '__main__':
    create_db()
