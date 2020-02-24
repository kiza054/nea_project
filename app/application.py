# Imports the app and db instance from __init__.py
from app import app, db
# Imports the User model from models.py
from app.models import User

@app.shell_context_processor
def shell_context():
    # Registers the items returned in the shell session
    return {'db': db, 'User': User}