from flask_wtf import FlaskForm
from wtforms import Form, PasswordField, StringField, SubmitField, SelectField

class StatsForm(FlaskForm):
    category = StringField('Category')
    submit = SubmitField('Add')

class StatsDD(FlaskForm):
    stats = SelectField('Stats')
    submit = SubmitField('Remove')

class LoginForm(Form):
    email = StringField('Email')
    password = PasswordField('Passw')
    submit = SubmitField('Login')
