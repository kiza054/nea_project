# System Imports
import os, requests
# Modular Imports
from werkzeug.urls import url_parse
from datetime import datetime, date
from flask_login import current_user, login_required, login_user, logout_user
from flask import render_template, flash, redirect, request, url_for
# Imports db instance from __init__.py
from app import db
# Imports bp variable from main/__init__.py
from app.main import bp
# Imports the User and Bus_stops from models.py
from app.models import User, Bus_stops
# Imports the EditProfielForm from main/forms.py
from app.main.forms import EditProfileForm

# Defines the homepage route
@bp.route('/')
@bp.route('/home') # Uses two endpoints as you can have / or /home in the browser
@login_required # Login is required to access this page
def home():
    # Returns the home.html template with the predefined user set
    user = current_user.username
    return render_template('index.html', title='Home', user=user)

# Defines the profile page
@bp.route('/user/<username>')
@login_required # Login is required to access this page
def user(username):
    # Queries database for the username that is logged in
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('account.html', title='User Profile', user=user)

# Defines the edit profile page
@bp.route('/user/<username>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    # Pulls in EditProfileForm from forms.py
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        # Swaps new username and email for old ones
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() # Adds them to database
        flash('Your changes have been saved')
        return redirect(url_for('main.edit_profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account_edit.html', title='Edit Profile', form=form, username=username)

# Defines the live timetables page
@bp.route('/live_timetable', methods=['GET', 'POST'])
def stops():
    number = request.form.get('stop_number', None) # Requests a stop number

    if number is None:
        stop_number = str(10001) # Defaults stop number to first bus stop (10001)
        stop_number_str = str(stop_number)
    else:
        stop_number = request.form['stop_number']
        stop_number_str = str(stop_number) # When user types in bus stop number then it changes the bus stop number

    now = datetime.now() # Uses current datetime from datetime module
    current_date = str(date.today()) # Uses current data from datetime module
    time = now.strftime("%H:%M") # Formats time to HH:MM
    # Requests JSON data for timetable from Transport API website (including set variables above)
    r = requests.get('https://transportapi.com/v3/uk/bus/stop/4500'+stop_number+'/'+current_date+'/'+time+'/timetable.json?app_id=3f8e34c8&app_key=eac525990f06429e85bab4aa9e5e4f29&group=no&limit=10')
    json_object = r.json() # Provides output as JSON data

    try:
        items = json_object['departures']['all']
        name = json_object['name']
        locality = json_object['locality']
        # Shows JSON data for selected categories above

    except KeyError:
        # Provides custom 404 error is bus stop couldn't be founds
        return render_template('errors/404_timetable_error.html', title = '404 Error')

    for item in items:
        line_name = item['line_name']
        direction = item['direction']
        time = item['aimed_departure_time']
        in_outbound = item['dir']
        operator = item['operator_name']
        operator_code = item['operator']
        # Creates a collection of items for timetable information

    return render_template('live_timetable.html', title='Live Timetable', items=items, name=name,
                locality=locality, stop_number_str=stop_number_str)

# Defines bus stops route
@bp.route('/bus_stops', methods=["GET", "POST"])
def bus_stops():
    stops = Bus_stops.query.all() # Database query for all bus stops in table
    return render_template('bus_stops.html', title='Bus Stop Details', stops=stops)

# Defines the moovit widget route
@bp.route('/moovit')
def moovit():
    return render_template('moovit.html', title='Moovit Journey Planner')