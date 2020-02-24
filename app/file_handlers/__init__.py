# Imports Blueprint from flask module
from flask import Blueprint

# Sets bp variable as a Blueprint package
bp = Blueprint('file_handlers', __name__)

# Imports file_handlers/downloads.py & uploads.py
from app.file_handlers import downloads, uploads