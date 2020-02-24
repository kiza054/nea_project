# Module imports
import os

class Config(object): # Class for all app settings
    # Secret Key defined to protect app from CSRF attacks
    SECRET_KEY = os.urandom(36).hex() or 'thisisasecret'
    # SQLALCHEMY_DATABASE_URI set to database location
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    # Modifications are being tracked
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Flask Admin theme
    FLASK_ADMIN_SWATCH = 'cyborg'