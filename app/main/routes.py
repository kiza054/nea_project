import os, requests
from werkzeug.urls import url_parse
from datetime import datetime, date
from flask_login import current_user, login_required, login_user, logout_user
from flask import render_template, flash, redirect, request, url_for

from app import db
from app.main import bp
from app.models import User, Bus_stops
from app.main.forms import EditProfileForm

@bp.route('/')
@bp.route('/home')
@login_required
def home():
    return render_template('index.html', title="Home")

@bp.route('/user/<username>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved', category='success')
        return redirect(url_for('main.edit_profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account_edit.html', title='Edit Profile', form=form, username=username)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('account.html', title='User Profile', user=user)

@bp.route('/live_timetable', methods=['GET', 'POST'])
def stops():
    number = request.form.get('stop_number', None)

    if number is None:
        stop_number = str(10001)
        stop_number_str = str(stop_number)
    else:
        stop_number = request.form['stop_number']
        stop_number_str = str(stop_number)

    now = datetime.now()
    current_date = str(date.today())
    time = now.strftime("%H:%M")
    r = requests.get('https://transportapi.com/v3/uk/bus/stop/4500'+stop_number+'/'+current_date+'/'+time+'/timetable.json?app_id=3f8e34c8&app_key=eac525990f06429e85bab4aa9e5e4f29&group=no&limit=10')
    json_object = r.json()

    try:
        items = json_object['departures']['all']
        name = json_object['name']
        locality = json_object['locality']

    except KeyError:
        return render_template('errors/404_timetable_error.html', title = '404 Error')

    for item in items:
        line_name = item['line_name']
        direction = item['direction']
        time = item['aimed_departure_time']
        in_outbound = item['dir']
        operator = item['operator_name']
        operator_code = item['operator']

    return render_template('live_timetable.html', title='Live Timetable', items=items, name=name,
                locality=locality, stop_number_str=stop_number_str)

@bp.route('/bus_stops', methods=["GET", "POST"])
def bus_stops():
    stops = Bus_stops.query.all()
    return render_template('bus_stops.html', title='Bus Stop Details', stops=stops)

@bp.route('/credits')
def credits():
    return render_template('credits.html', title='Credits')

@bp.route('/moovit')
def moovit():
    return render_template('moovit.html', title='Moovit Journey Planner')