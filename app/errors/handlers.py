from app import db
from app.errors import bp
from flask import render_template

@bp.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html', title='403 Error'), 403

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', title='404 Error'), 404

@bp.errorhandler(413)
def entity_too_large(error):
    return render_template('errors/413.html', title='413 Error'), 413

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html', title='500 Error'), 500