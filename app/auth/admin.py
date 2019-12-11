import flask_login as login
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request, flash

class AdminView(ModelView):
    can_export = True
    page_size = 50
    column_exclude_list = ['password_hash']
    column_searchable_list = ['username', 'email']
    column_editable_list = ['username', 'email', 'is_admin']
    create_modal = True
    edit_modal = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return login.current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            flash('403: Sorry, you don\'t have access to this page.', category='error')
            return redirect(url_for('home'))

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