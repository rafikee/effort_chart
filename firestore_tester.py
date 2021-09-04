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

data = db.collection('charts').document('123').get().to_dict() # get dictionary from document
db.collection('charts').document().set(data) # create a new doc with auto gen key

# Create a reference to the cities collection
charts = db.collection('charts')

# Create a query against the collection
q = charts.where('brand', '==', 'vcu')