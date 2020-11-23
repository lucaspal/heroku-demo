import os

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/environment')
def get_environment():
    env_name = os.getenv('environment') or 'local'
    return f'Env. name: {env_name}'


if __name__ == '__main__':
    app.run()
