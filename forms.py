from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class StatsForm(FlaskForm):
    category = StringField('Category')
    submit = SubmitField('Submit')

class StatsDD(FlaskForm):
    stats = SelectField('Stats')
    submit_remove = SubmitField('Submit')
