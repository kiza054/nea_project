# Imports db instance from __init__.py
from app import db
# Imports bp variable from auth/__init__.py
from app.auth import bp
# Imports User model from models.py
from app.models import User
# Imports LoginForm and RegistrationForm from auth/forms.py
from app.auth.forms import LoginForm, RegistrationForm
# Modular Imports
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask import render_template, redirect, url_for, flash, request

# Defines the login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # Checks to see if user is logged in
        return redirect(url_for('main.home'))
    form = LoginForm() # Use of LoginForm brought in from forms.py
    if request.method == 'POST': # Checks if the form submits a POST request
        # Queries database to see if the user trying to log in is inside database
        user = User.query.filter_by(username=form.username.data).first()
        # Checks to see is the password matches one inside database
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password, Please try again')
            return redirect(url_for('auth.login'))
        # If password matches then it logs the user in
        login_user(user, remember=form.remember_me.data)
        # Generates next page that app will redirect to
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            flash('Successfully Logged In')
            # Flashes sucess message and logs user in
            next_page = url_for('main.home')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

# Defines the register route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST': # Checks if the form submits a POST request
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data) # Sets password to users defined password
        db.session.add(user) # Adds data from user variable above into database
        db.session.commit() # Commits data to database
        flash('User {} Registered'.format(form.username.data))
        return redirect(url_for('auth.login')) # Redirects to login once process is complete
    return render_template('register.html', title='Register', form=form)

# Defines the logout route
@bp.route('/logout')
def logout():
    logout_user() # Logs user out
    # Then redirects to login page
    return redirect(url_for('auth.login'))