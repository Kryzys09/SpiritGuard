from django.shortcuts import render
from SpiritGuard.settings import config
from alcohols.calculations import *
import pyrebase
import datetime


firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
# Create your views here.


def render_calculator(request):
    user = request.session['user']
    user_data = db.child('users').child(user['localId']).get().val()
    print("USER DATA: ", user_data)
    drinks = get_drinks(user_data['logs'])
    if user_data['gender'] == "male":
        gender = 1
    else:
        gender = 0
    bac = blood_alcohol_content(gender, drinks, user_data['weight'], 1)
    mai = max_alcohol_intake(gender, datetime.datetime.now() + datetime.timedelta(hours=8), datetime.datetime.now(), bac)
    data = {
        'bac':  "{:.3f}".format(bac),
        'sobering_time': sobering_time_projection(15, gender, bac).popitem()[0],
        'max_alcohol_intake': mai,
        'translate_bac': translate_bac(gender, user_data['weight'], mai, classic_alcohols),
        'gender': gender,
        'weight': user_data['weight'],
        'drinks': drinks
    }
    return render(request, 'calculator.html', data)


def get_logs(user):
    logs = db.child('users').child(user['localId']).child('logs').get().val()
    return logs


def get_drinks(logs):
    drinks = []
    for key in logs:
        drinks.append(Alcohol(logs[key]['name'], logs[key]['volume'], logs[key]['percentage']))
    return drinks



