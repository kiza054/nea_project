# Module Imports
import flask_login as login
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request, flash

# Defines AdminView class
class AdminView(ModelView):
    can_export = True # Allows export as CSV
    page_size = 50 # Shows 50 entries per page
    column_exclude_list = ['password_hash'] # Doesn't show password
    column_searchable_list = ['username'] # Allows searching of username
    column_editable_list = ['is_admin'] # Allows admin to change who is/is not admin
    create_modal = True
    edit_modal = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    # Admin page only accessible is user is admin
    def is_accessible(self):
        return login.current_user.is_admin

    # Does not allow users who are not admin into admin page
    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            flash('403: Sorry, you don\'t have access to this page.')
            return redirect(url_for('main.user', username=current_user.username))

class Bus_stopsView(ModelView):
    can_export = True
    page_size = 10
    column_searchable_list = ['stop_id', 'stop_name', 'town']
    column_editable_list = ['stop_name', 'town']
    column_exclude_list = ['x', 'y', 'z']
    create_modal = True
    edit_modal = True

class TimetableView(ModelView):
    can_export = True
    page_size = 10
    column_searchable_list = ['name', 'service_number', 'operator']
    column_editable_list = ['name', 'service_number', 'operator']
    column_exclude_list = ['file_path']
    create_modal = True
    edit_modal = True

class NetworkMapsView(ModelView):
    can_export = True
    page_size = 10
    column_searchable_list = ['name', 'operator']
    column_editable_list = ['name', 'operator']
    column_exclude_list = ['data']
    create_modal = True
    edit_modal = True