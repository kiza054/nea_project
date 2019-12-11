from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Bus_stops(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    stop_id = db.Column(db.Integer(), nullable=False, unique=True)
    stop_name = db.Column(db.String(), nullable=False)
    town = db.Column(db.String(), nullable=False)
    x = db.Column(db.String(), nullable=False)
    y = db.Column(db.String(), nullable=False)
    z = db.Column(db.String(), nullable=False)
    photo_front = db.Column(db.String(), nullable=False)
    photo_side = db.Column(db.String(), nullable=False)

class NetworkMaps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operator = db.Column(db.String(300))
    name = db.Column(db.String(300))
    file_path = db.Column(db.String(300), nullable=False)

class Timetables(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    service_number = db.Column(db.Integer)
    operator = db.Column(db.String(300))
    file_path = db.Column(db.String(300), nullable=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))