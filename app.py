#!/usr/bin/env python3
from flask import Flask

api = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="ATLanta1904",
    hostname="localhost",
    databasename="prueba",
)

api.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

if __name__ == '__main__':
    from endpoints.tasks import *

    api.run(debug=True)
