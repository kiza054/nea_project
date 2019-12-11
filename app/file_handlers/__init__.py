from flask import Blueprint

bp = Blueprint('file_handlers', __name__)

from app.file_handlers import downloads, uploads