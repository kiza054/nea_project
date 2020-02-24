# Imports Blueprint from flask module
from flask import Blueprint

# Sets bp variable as a Blueprint package
bp = Blueprint('auth', __name__)

# Imports auth/routes.py
from app.auth import routes