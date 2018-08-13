from flask import Flask

api = Flask(__name__)

if __name__ == '__main__':
    from endpoints.tasks import *
    api.run(host="0.0.0.0", port=5000, debug=True)

