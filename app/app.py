from flask import Flask
import pymysql

api = Flask(__name__)


def create_db():
    try:
        pymysql.connect(user="hernanbosqued", passwd="ATLanta1904", db="prueba")

    except Exception:
        conn = pymysql.connect(user="hernanbosqued", passwd="ATLanta1904")
        with conn.cursor() as cursor:
            cursor.execute('create database IF NOT EXISTS prueba')
            cursor.execute('create table IF NOT EXISTS prueba.tasks (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, ' +
                           'title VARCHAR(50) NULL, ' +
                           'description VARCHAR(500) NULL, ' +
                           'done BOOLEAN)')


if __name__ == '__main__':
    create_db()
    from endpoints.tasks import *
    api.run(host="localhost", port=5000, debug=True)

