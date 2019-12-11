import os
from app import app
from flask import render_template, request, flash, send_from_directory

from app.file_handlers import bp
from app.models import Timetables, NetworkMaps

@bp.route('/downloads')
def downloadspage():
    return render_template('downloads.html', title='Downloads')

@bp.route('/downloads/timetables')
def download_timetables():
    timetables = Timetables.query.all()
    return render_template('download_timetables.html', title='Download Timetables', timetables=timetables)

@bp.route('/downloads/timetables/<filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@bp.route('/downloads/networkmaps')
def downloadnetworkmaps():
    operators = NetworkMaps.query.all()
    return render_template('download_networkmaps.html', title='Download Network Maps', operators=operators)

@bp.route('/downloads/networkmaps/<filename>', methods=['GET', 'POST'])
def download_networkmaps(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_2'], filename, as_attachment=True)