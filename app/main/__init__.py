# Imports Blueprint from flask module
from flask import Blueprint

# Sets bp variable as a Blueprint package
bp = Blueprint('main', __name__)

# Imports main/routes.py
from app.main import routes