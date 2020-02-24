# Module imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class UploadTimetablesForm(FlaskForm):
    service_number = StringField('Service Number', validators=[DataRequired()])
    operator = StringField('Operator', validators=[DataRequired(), Length(min=1, max=40)])
    submit = SubmitField('Submit')

class UploadNetworkMapsForm(FlaskForm):
    operator = StringField('Operator', validators=[DataRequired(), Length(min=1, max=40)])
    submit = SubmitField('Submit')