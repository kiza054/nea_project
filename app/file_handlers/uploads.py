# System Imports
import os
# Imports app and db instance from __init__.py
from app import app, db
# Imports bp variable from file_handlers/__init__.py
from app.file_handlers import bp
# Modular Imports
from werkzeug.utils import secure_filename
from flask_login import login_required
from flask import render_template, flash, redirect, request, url_for
# Imports Timetables and NetworkMaps model from models.py
from app.models import NetworkMaps, Timetables
# Imports UploadNetworkMapsForm and UploadTimetablesForm from file_handlers/forms.py
from app.file_handlers.forms import UploadNetworkMapsForm, UploadTimetablesForm

# Upload folders for uploads
UPLOAD_FOLDER = ("C:/Programming/Python/Flask/nea_project/app/static/pdf_files/timetables/")
UPLOAD_FOLDER_2 = ("C:/Programming/Python/Flask/nea_project/app/static/pdf_files/network_maps/")
# Configurations for upload folders
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_2

# Defines the upload network maps route
@bp.route('/uploadnetworkmaps', methods=['GET', 'POST'])
@login_required
def upload():
    return render_template('uploadnetworkmaps.html', title='Upload Network Maps')

# Defines the upload timetables route
@bp.route('/uploadtimetables', methods=['GET', 'POST'])
@login_required
def uploadtimetable():
    return render_template('uploadtimetable.html', title='Upload Timetables')

# Defines the confirmation route for network maps
@bp.route('/uploadconfirmation/networkmaps', methods=['GET', 'POST'])
def fileupload():
    if request.method =='POST': # Accepts POST requests only
        file = request.files['inputFile'] # Requests file from form
        if file:
            filename = secure_filename(file.filename) # Makes filename a secure filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER_2'],filename)) # Creates the file_path
            newFile = NetworkMaps(name=filename, operator=request.form.get("operator"),
                file_path=os.path.join(app.config['UPLOAD_FOLDER_2'], filename))
            db.session.add(newFile) # Saves newFile into database
            db.session.commit()
            flash('Saved ' + file.filename + ' to the Network Maps database!', category='success')
        else:
            flash('404: File not recognised, please fill out the form again.', category='error')
    return render_template('uploadnetworkmaps.html', title='Confirmation')

# Defines the confirmation route for timetables
@bp.route('/uploadconfirmation/timetables', methods=['GET', 'POST'])
def fileuploadtimetable():
    if request.method =='POST' and request.form: # Accepts POST requests only
        file = request.files['inputFile'] # Requests file from form
        if file:
            filename = secure_filename(file.filename) # Makes filename a secure filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) # Creates the file_path
            newFile = Timetables(name=filename, operator=request.form.get("operator"),
                service_number=request.form.get("service_number"),
                file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.session.add(newFile) # Saves newFile into database
            db.session.commit()
            flash('Saved ' + file.filename + ' to the Timetables database!', category='success')
        else:
            flash('404: File not recognised, please fill out the form again.', category='error')
    return render_template('uploadtimetable.html', title='Confirmation')