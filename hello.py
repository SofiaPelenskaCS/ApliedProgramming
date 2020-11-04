from flask import Flask
app = Flask(__name__)


PREFIX = "/api/v1/hello-world-21"

@app.route(PREFIX + '/')
def hello_world():
    return 'Hello, World! 21'