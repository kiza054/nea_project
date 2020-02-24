# Imports Blueprint from flask module
from flask import Blueprint

# Sets bp variable as a Blueprint package
bp = Blueprint('errors', __name__)

# Imports errors/handlers.py
from app.errors import handlers