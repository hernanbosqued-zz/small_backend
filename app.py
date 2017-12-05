from flask import Flask

api = Flask(__name__)

if __name__ == '__main__':
    from tasks import *
    api.run(debug=True)
