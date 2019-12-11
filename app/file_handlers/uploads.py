import os
from app import app, db
from app.file_handlers import bp
from werkzeug.utils import secure_filename
from flask import render_template, flash, redirect, request, url_for

from app.models import NetworkMaps, Timetables
from app.main.forms import UploadNetworkMapsForm, UploadTimetablesForm

UPLOAD_FOLDER = '/home/ubuntu/nea_project/app/static/pdf_files/timetables/'
UPLOAD_FOLDER_2 = '/home/ubuntu/nea_project/app/static/pdf_files/network_maps/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_2

@bp.route('/uploadnetworkmaps', methods=['GET', 'POST'])
def upload():
    return render_template('uploadnetworkmaps.html', title='Upload Network Maps')

@bp.route('/uploadtimetables', methods=['GET', 'POST'])
def uploadtimetable():
    return render_template('uploadtimetable.html', title='Upload Timetables')

@bp.route('/uploadconfirmation/networkmaps', methods=['GET', 'POST'])
def fileupload():
    if request.method =='POST':
        file = request.files['inputFile']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_2'],filename))
            newFile = NetworkMaps(name=filename, operator=request.form.get("operator"),
                file_path=os.path.join(app.config['UPLOAD_FOLDER_2'], filename))
            db.session.add(newFile)
            db.session.commit()
            flash('Saved ' + file.filename + ' to the Network Maps database!', category='success')
        else:
            flash('404: File not recognised, please fill out the form again.', category='error')
    return render_template('uploadnetworkmaps.html', title='Confirmation')

@bp.route('/uploadconfirmation/timetables', methods=['GET', 'POST'])
def fileuploadtimetable():
    if request.method =='POST' and request.form:
        file = request.files['inputFile']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            newFile = Timetables(name=filename, operator=request.form.get("operator"),
                service_number=request.form.get("service_number"),
                file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.session.add(newFile)
            db.session.commit()
            flash('Saved ' + file.filename + ' to the Timetables database!', category='success')
        else:
            flash('404: File not recognised, please fill out the form again.', category='error')
    return render_template('uploadtimetable.html', title='Confirmation')