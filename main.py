from flask import Flask, request, render_template, url_for, redirect
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from forms import StatsForm, StatsDD

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'blabla'

@app.route('/form')
def my_form():
    check_fire_db() # initialize the firebase app
    db = firestore.client() # get the db object
    chart_ref = db.collection('charts').document('test') # get the chart object
    chart = chart_ref.get().to_dict() # get it as dict
    stats = chart['stats']
    return render_template('form.html', stats=stats)

@app.route('/form', methods=['POST'])
def my_form_post():
    check_fire_db() # initialize the firebase app
    db = firestore.client() # get the db object
    text = request.form['text']
    chart_ref = db.collection('charts').document('test') # get the chart object
    chart_ref.update({'stats': firestore.ArrayUnion([text])})
    return redirect(url_for('fire'))

@app.route('/wtf', methods=('GET', 'POST'))
def wtf():
    form = StatsForm()
    check_fire_db() # initialize the firebase app
    db = firestore.client() # get the db object
    chart_ref = db.collection('charts').document('test') # get the chart object
    if form.is_submitted():
        result = form.category.data
        chart_ref.update({'stats': firestore.ArrayUnion([result])})
        return redirect(url_for('fire'))
    chart = chart_ref.get().to_dict() # get it as dict
    stats = chart['stats']
    return render_template('forms.html', form=form, stats=stats)

@app.route('/remove', methods=('GET', 'POST'))
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
        return redirect(url_for('fire'))
    return render_template('forms_remove.html', form=form)

# firebase
@app.route('/', methods=['GET', 'POST'])
def fire():
    check_fire_db() # initialize the firebase app
    db = firestore.client() # get the db object
    chart_ref = db.collection('charts').document('test') # get the chart object
    chart = chart_ref.get().to_dict() # get it as dict

    stats = chart['stats']
    players = chart['players']
    return render_template('chart.html', plyrs=players, stats=stats)

# initialize the firebase app
def check_fire_db():
    if not firebase_admin._apps:
        if os.getenv('FLASK_ENV') == 'development':
            cred = credentials.Certificate('key.json')
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()
    return

# test
@app.route('/test', methods=['GET'])
def test():
    return 'test'

# local json
@app.route('/old', methods=['GET'])
def hello():
    with open('chart_input.json') as f:
        data = json.load(f)
    stats = data['stats']
    players = data['players']
    return render_template('chart.html', plyrs=players, stats=stats)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
