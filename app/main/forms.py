from app.models import User
from flask import abort, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=40)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

class UploadTimetablesForm(FlaskForm):
    service_number = StringField('Service Number', validators=[DataRequired()])
    operator = StringField('Operator', validators=[DataRequired(), Length(min=1, max=40)])
    submit = SubmitField('Submit')

class UploadNetworkMapsForm(FlaskForm):
    operator = StringField('Operator', validators=[DataRequired(), Length(min=1, max=40)])
    submit = SubmitField('Submit')