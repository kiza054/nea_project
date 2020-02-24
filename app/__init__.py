# System imports
import logging, os
# Imports necessary at the top of the file
from flask import Flask
from config import Config
from flask_admin import Admin
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from logging.handlers import RotatingFileHandler

app = Flask(__name__) # Instantiates app as the main package for the app
app.config.from_object(Config) # Pulls in configurations for app
db = SQLAlchemy(app) # Creates db instance
migrate = Migrate(app, db, render_as_batch=True) # Creates migrate instance
bootstrap = Bootstrap(app) # Creates bootstrap instance
login = LoginManager(app) # Creates login instance
fonts = FontAwesome(app) # Creates fonts instance
login.login_view = 'auth.login' # Creates a login view that points to login route
login.login_message = ('Please log in to access this page')

from app.main import bp as main_bp
# Main Blueprint
app.register_blueprint(main_bp)

from app.errors import bp as errors_bp
# Errors Blueprint
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
# Auth Blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.file_handlers import bp as files_bp
# File_handlers Blueprint
app.register_blueprint(files_bp)

# Imports the models from routes.py
from app import models

# Imports model classes from models.py
from app.models import User, Bus_stops, Timetables, NetworkMaps
# Imports admin classes from admin.py
from app.auth.admin import AdminView, Bus_stopsView, TimetableView, NetworkMapsView

#  Creates admin dashboard that defaults to the Users page
admin = Admin(app, name='WYJP Admin Dashboard', template_mode='bootstrap3', 
    index_view=AdminView(User, db.session, url='/admin', endpoint='admin'))
admin.add_view(Bus_stopsView(Bus_stops, db.session))
admin.add_view(TimetableView(Timetables, db.session))
admin.add_view(NetworkMapsView(NetworkMaps, db.session))
admin.add_link(MenuLink(name='Back to Homepage', category='', url='/'))

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs') # Creates the 'logs' folder if it doesn't exist
# Creates files with error messages inside the logs folder
file_handler = RotatingFileHandler('logs/wyjp_debugging.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('WYJP startup')

if __name__ == "__main__":
    app.run(debug=True) # Runs application with debug mode on