from flask import Flask

api = Flask(__name__)

if __name__ == '__main__':
    from endpoints.tasks import *

    api.run(debug=True)
