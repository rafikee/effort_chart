from flask import Flask, request, render_template, url_for, redirect
import pyrebase
import json
import firebase_admin
from firebase_admin import credentials, firestore
import os
from forms import StatsForm, StatsDD, LoginForm
import flask_login
from flask_login import current_user, login_user, LoginManager, UserMixin, login_required
import pandas as pd

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login = LoginManager(app)
firebase = pyrebase.initialize_app(json.load(open('fbconfig.json')))

class User(UserMixin):
    def get_brand(self):
        return text_type(self.brand)

@login.user_loader
def user_loader(email):
    user = User()
    user.id = email
    user.brand = db.collection('users').document(user.id).get().to_dict()['brand']
    return user

@login.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))

# Update this so it displays errors in html on the page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('charts'))
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
            return redirect(url_for('charts'))
        except:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

@app.route('/chart/<chart>/add', methods=('GET', 'POST'))
@login_required
def add(chart):
    form = StatsForm()
    chart_ref = db.collection(current_user.brand).document(chart) # get the chart object
    if form.is_submitted():
        result = form.category.data
        chart_ref.update({'stats': firestore.ArrayUnion([result])})
        return redirect(url_for('chart', chart_name=chart))
    chart = chart_ref.get().to_dict() # get it as dict
    stats = chart['stats']
    return render_template('add.html', form=form, stats=stats)

@app.route('/chart/<chart>/remove', methods=('GET', 'POST'))
@login_required
def remove(chart):
    form = StatsDD()
    chart_ref = db.collection(current_user.brand).document(chart) # get the chart object
    chart = chart_ref.get().to_dict() # get it as dictrp
    stats = chart['stats']
    form.stats.choices = stats
    if form.is_submitted():
        result = form.stats.data
        chart_ref.update({'stats': firestore.ArrayRemove([result])})
        return redirect(url_for('chart', chart_name=chart))
    return render_template('remove.html', form=form)

@app.route('/chart/<chart_id>', methods=['GET', 'POST'])
@login_required
def chart(chart_id):
    # for updating the chart name
    if request.method == 'POST':
        print(request.get_json())
        return "nothing"
    event_id = request.args['event_id']
    data = db.collection('charts').document(chart_id).collection('stats').document(event_id).get().to_dict()
    event_name = data['name']
    data = data['stats']
    df = pd.DataFrame.from_dict(data, orient='index')
    categories = list(df)
    player_names = list(df.index.values)
    players = []
    for plyr in player_names:
        players.append({'name': plyr, 'stats' : list(df.loc[plyr])})
    return render_template('chart.html', plyrs=players, categories=categories, event_name=event_name)

@app.route('/charts', methods=['GET', 'POST'])
@login_required
def charts():
    brand = current_user.brand
    charts = [(chart.id, chart.to_dict()['name']) for chart in db.collection('charts').where('brand', '==', brand).get()]
    '''if not charts:
        create_chart(brand)
        charts = [chart.id for chart in db.collection('charts').where('brand', '==', brand).get()]'''
        # clean this up, the logic when someone doesn't have a chart
    return render_template('charts.html', charts=charts)

@app.route('/chart/<chart_id>/events', methods=['GET', 'POST'])
@login_required
def events(chart_id):
    events = [(event.id, event.to_dict()['name']) for event in db.collection('charts').document(chart_id).collection('stats').get()]
    chart_name = db.collection('charts').document(chart_id).get().to_dict()['name']
    data = {
        'chart' : chart_id,
        'events' : events,
        'chart_name' : chart_name,
    }
    return render_template('events.html', data=data)

@app.route('/chart/<chart_id>/create_event', methods=['GET', 'POST'])
@login_required
def create_event(chart_id):
    event_id = request.args['event_id']
    data = db.collection('charts').document(chart_id).collection('stats').document(event_id).get().to_dict()
    event_id = db.collection('charts').document(chart_id).collection('stats').add(data)[1].id
    return redirect(url_for('chart', chart_id=chart_id, event_id=event_id))

# initialize the firebase app
def check_fire_db():
    if not firebase_admin._apps:
        if os.getenv('FLASK_ENV') == 'development':
            cred = credentials.Certificate('key.json')
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()
    return

# these need to happen after all the functions
check_fire_db() # initialize the firebase app
db = firestore.client() # get the db objects

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.