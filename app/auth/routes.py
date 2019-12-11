from app import db
from app.auth import bp
from app.models import User
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user
from flask import render_template, redirect, url_for, flash, request

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password, Please try again.', category='error')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            flash('Successfully Logged In', category='success')
            next_page = url_for('main.home')
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} Registered'.format(form.username.data), category='success')
        return redirect(url_for('home'))
    return render_template('auth/register.html', title='Register', form=form)