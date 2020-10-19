from flask import Flask, request, render_template, url_for, redirect
import pyrebase
import json
import firebase_admin
from firebase_admin import credentials, firestore
import os
from forms import StatsForm, StatsDD, LoginForm
import flask_login
from flask_login import current_user, login_user, LoginManager, UserMixin

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login = LoginManager(app)
firebase = pyrebase.initialize_app(json.load(open('fbconfig.json')))

class User(UserMixin):
    pass

@login.user_loader
def user_loader(email):
    user = User()
    user.id = email
    return user

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))

# Update this so it displays errors in html on the page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chart'))
    auth = firebase.auth()
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        try:
            login = auth.sign_in_with_email_and_password(email, password)
            user = User()
            user.id = email
            login_user(user)
            return redirect(url_for('chart'))
        except:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

@app.route('/add', methods=('GET', 'POST'))
@flask_login.login_required
def add():
    form = StatsForm()
    check_fire_db() # initialize the firebase app
    db = firestore.client() # get the db object
    chart_ref = db.collection('charts').document('test') # get the chart object
    if form.is_submitted():
        result = form.category.data
        chart_ref.update({'stats': firestore.ArrayUnion([result])})
        return redirect(url_for('chart'))
    chart = chart_ref.get().to_dict() # get it as dict
    stats = chart['stats']
    return render_template('add.html', form=form, stats=stats)

@app.route('/remove', methods=('GET', 'POST'))
@flask_login.login_required
def remove():
    form = StatsDD()
    check_fire_db() # initialize the firebase app
    db = firestore.client() # get the db object
    chart_ref = db.collection('charts').document('test') # get the chart object
    chart = chart_ref.get().to_dict() # get it as dict
    stats = chart['stats']
    form.stats.choices = stats
    if form.is_submitted():
        result = form.stats.data
        chart_ref.update({'stats': firestore.ArrayRemove([result])})
        return redirect(url_for('chart'))
    return render_template('remove.html', form=form)

@app.route('/chart', methods=['GET', 'POST'])
@flask_login.login_required
def chart():
    check_fire_db() # initialize the firebase app
    db = firestore.client() # get the db object
    chart_ref = db.collection('charts').document('test') # get the chart object
    chart = chart_ref.get().to_dict() # get it as dict

    stats = chart['stats']
    players = chart['players']
    stats_print = []
    for stat in stats:
        stats_print.append(stat.replace(" ", "_"))
    return render_template('chart.html', plyrs=players, stats=stats, stats_print=stats_print)

# initialize the firebase app
def check_fire_db():
    if not firebase_admin._apps:
        if os.getenv('FLASK_ENV') == 'development':
            cred = credentials.Certificate('key.json')
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()
    return

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
