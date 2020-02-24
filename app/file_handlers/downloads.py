# System Imports
import os
# Imports app instance from __init__.py
from app import app
# Imports bp variable from file_handlers/__init__.py
from app.file_handlers import bp
# Modular Imports
from flask import render_template, request, flash, send_from_directory
# Imports Timetables and NetworkMaps model from models.py
from app.models import Timetables, NetworkMaps

# Route for downloads homepage
@bp.route('/downloads')
def downloads_page():
    return render_template('downloads.html', title='Downloads')

# Route for showing available timetables for download
@bp.route('/downloads/timetables')
def download_timetables():
    timetables = Timetables.query.all() # Shows all timetables in database
    return render_template('download_timetables.html', title='Download Timetables', timetables=timetables)

# Route for downloading available timetables
@bp.route('/downloads/timetables/<filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Route for showing available network maps for download
@bp.route('/downloads/networkmaps')
def downloadnetworkmaps():
    operators = NetworkMaps.query.all() # Shows all network maps in database
    return render_template('download_networkmaps.html', title='Download Network Maps', operators=operators)

# Route for downloading available network maps
@bp.route('/downloads/networkmaps/<filename>', methods=['GET', 'POST'])
def download_networkmaps(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_2'], filename, as_attachment=True)