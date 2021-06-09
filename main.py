import os

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

app = Flask(__name__)

env_name = os.getenv('environment') or 'local'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if env_name == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.debug = True

db = SQLAlchemy(app)

# TODO: Replace with a proper `setup.py` script.
db.create_all()


@dataclass
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return 'User: %r' % self.username


@app.route('/')
def hello_world():
    return 'Hello, World this is a demo about interesting stuff!'


@app.route('/environment')
def get_environment():
    current_environment = os.getenv('environment') or 'local'
    return f'Env. name: {current_environment}'


@app.route('/user/new')
def create_user():
    try:
        guest = User(username='guest', email='guest@example.com')
        db.session.add(guest)
        db.session.commit()
        new_user_id = guest.id
        return make_response(jsonify(user_id=new_user_id))
    except Exception as e:
        return make_response(jsonify(error=str(e)), 500)


@app.route('/users')
def get_users():
    users = User.query.all()
    return make_response(jsonify(all_users=[user.__repr__() for user in users]))


if __name__ == '__main__':
    app.run()
