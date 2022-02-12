from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length


class ReportForm(FlaskForm):
    bin_id = StringField(label='Bin ID', render_kw={'readonly': True})

    desc = TextAreaField('Problem Description', [InputRequired(), Length(
        max=200, message='Description of problem must be under 200 characters long.')])
