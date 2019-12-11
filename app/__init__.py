import os
import logging
from config import Config
from flask_mail import Mail
from flask_admin import Admin
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin.menu import MenuLink
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from flask import Flask, url_for, redirect
from flask_admin.contrib.sqla import ModelView
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')
bootstrap = Bootstrap(app)
fonts = FontAwesome(app)

from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.file_handlers import bp as files_bp
app.register_blueprint(files_bp)

from app import models
from app.models import User, Bus_stops, Timetables, NetworkMaps
from app.auth.admin import AdminView, Bus_stopsView, TimetableView, NetworkMapsView

admin = Admin(app, name='WYJP Admin Dashboard', template_mode='bootstrap3', index_view=AdminView(User,
                                                            db.session, url='/admin', endpoint='admin'))
admin.add_view(Bus_stopsView(Bus_stops, db.session))
admin.add_view(TimetableView(Timetables, db.session))
admin.add_view(NetworkMapsView(NetworkMaps, db.session))
admin.add_link(MenuLink(name='Back to Homepage', category='', url='/'))

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
file_handler = RotatingFileHandler('logs/wyjp_log.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('WYJP startup')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)