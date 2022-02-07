from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import Email, InputRequired, Length, ValidationError

from ..models import User


class ViewForm(FlaskForm):
    username = StringField(label='Username', render_kw={'readonly': True})
    email = StringField(label='Email Address', render_kw={'readonly': True})
    created = StringField(label='Created At', render_kw={'readonly': True})


class EditForm(FlaskForm):
    username = StringField('Username', [InputRequired(), Length(
        min=4, max=25, message='Username must be between 4 and 25 characters long.')])

    def validate_username(form, field):
        if form.username.data == current_user.username:
            return
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

    email = StringField('Email Address', [InputRequired(), Email()])

    def validate_email(form, field):
        if form.email.data == current_user.email:
            return
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')
