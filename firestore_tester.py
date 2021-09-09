from flask import Flask, request, render_template, url_for, redirect
import pyrebase
import json
import firebase_admin
from firebase_admin import credentials, firestore
import os
from forms import StatsForm, StatsDD, LoginForm
import flask_login
from flask_login import current_user, login_user, LoginManager, UserMixin, login_required

SECRET_KEY = os.urandom(32)
firebase = pyrebase.initialize_app(json.load(open('fbconfig.json')))

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

# data = db.collection('charts').document('EGycXeh60lfXSGlYjC5Q').get().to_dict() # get dictionary from document
# data = db.collection('charts').document('EGycXeh60lfXSGlYjC5Q').collection('stats').document('oaoQzhEc8daB7eFJzyeR').get().to_dict() # get dictionary from document

charts = db.collection('charts')
#q = charts.where('brand', '==', 'vcu').get()


#charts = [(chart.id, chart.to_dict()['name']) for chart in db.collection('charts').where('brand', '==', brand).get()]

charts.get()['']

new_data = {
    'name': 'practice 1',
    'stats' :
    {
        'Aaron': {'Deflection': 1, 'Rebound': 5, 'Steal': 3},
        'Rob': {'Steal': 4, 'Deflection': 3, 'Rebound': 2}
    }
}

db.collection('charts').document('EGycXeh60lfXSGlYjC5Q').collection('stats').document('oaoQzhEc8daB7eFJzyeR').set(new_data) # create a new doc with auto gen key
db.collection('charts').document('EGycXeh60lfXSGlYjC5Q').collection('stats').get()