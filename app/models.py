# Module imports
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# Imports the db and login instance from __init__.py
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Nullable = False means that data has to be in the table
    # Unique = True means that each database entry for username has to be unique

    # Creates unique avatar for each user
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        # Returns username and email
        return f"User('{self.username}', '{self.email}')"

    # Sets SHA-256 encrypton for users password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checks password against hashed password in database
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Bus_stops(db.Model): # Model for bus stops
    id = db.Column(db.Integer, unique=True, primary_key=True) # Primary Key
    stop_id = db.Column(db.Integer(), nullable=False, unique=True)
    stop_name = db.Column(db.String(), nullable=False)
    town = db.Column(db.String(), nullable=False)
    x = db.Column(db.String(), nullable=False)
    y = db.Column(db.String(), nullable=False)
    z = db.Column(db.String(), nullable=False)
    photo_front = db.Column(db.String(), nullable=False)
    photo_side = db.Column(db.String(), nullable=False)

    # Nullable = False means that data has to be in the table
    # Unique = True means that each database entry for stop_id and stop_name has to be unique

class NetworkMaps(db.Model): # Model for Network Maps
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    operator = db.Column(db.String(300))
    name = db.Column(db.String(300))
    file_path = db.Column(db.String(300), nullable=False)

    # Nullable = False means that data has to be in the table
    # Unique = True means that each database entry for stop_id and stop_name has to be unique

class Timetables(db.Model): # Model for Timetables
    id = db.Column(db.Integer, primary_key=True) # Primary Key
    name = db.Column(db.String(300))
    service_number = db.Column(db.Integer)
    operator = db.Column(db.String(300))
    file_path = db.Column(db.String(300), nullable=False)

    # Nullable = False means that data has to be in the table
    # Unique = True means that each database entry for stop_id and stop_name has to be unique

@login.user_loader
def load_user(id):
    return User.query.get(int(id))