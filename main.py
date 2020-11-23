import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/environment')
def get_environment():
    env_name = os.getenv('environment') or 'local'
    return f'Env. name: {env_name}'


@app.route('/user/new')
def create_user():
    try:
        guest = User(username='guest', email='guest@example.com')
        db.session.add(guest)
        db.session.commit()
    except Exception as e:
        print(e)

    return 'ok'


if __name__ == '__main__':
    app.run()
