from flask import Flask
from flask_restful import Api

from controller import *

app = Flask(__name__)
Api.add_resource(UserController,'/users')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
