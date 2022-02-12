from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import (Email, EqualTo, InputRequired, Length,
                                ValidationError)

from ..models import User


class DriverForm(FlaskForm):
    username = StringField('Username', [InputRequired(), Length(
        min=4, max=25, message='Username must be between 4 and 25 characters long.')])

    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

    email = StringField(
        'Email Address', [InputRequired(), Email()])

    def validate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    password = PasswordField('New Password', [InputRequired(), EqualTo(
        'confirm', message='Passwords must match.')])
    confirm = PasswordField('Repeat Password')
