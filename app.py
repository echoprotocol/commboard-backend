from flask import Flask
import config


app = Flask(__name__)


@app.route('/')
def hello_world():
    return('Hello, World!')
