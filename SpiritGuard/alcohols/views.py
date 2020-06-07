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
    if 'logs' in user_data.keys():
        drinks = get_drinks(user_data['logs'])
    else:
        drinks = []
    if user_data['gender'] == "M":
        gender = 0
    else:
        gender = 1
    rel_drinks = get_relevant_drinks(gender, user_data['weight'], drinks)
    if len(rel_drinks) > 0:
        start_date = datetime.datetime.strptime(rel_drinks[0].date, "%d-%m-%Y %H:%M")
        time = datetime.datetime.now() - start_date
        hours = time.total_seconds()/360
    else:
        hours = 0
        
    bac = blood_alcohol_content(gender, rel_drinks, user_data['weight'], hours)
    get_sober_date(gender, bac)
    now = datetime.datetime.now() + datetime.timedelta(hours=2)
    then = now + datetime.timedelta(hours=8)
    mai = max_alcohol_intake(gender, then, now, bac)
    if mai < 0:
        mai_send = "Impossible to sober up"
    else:
        mai_send = "{:.3f}".format(mai)
    bmi = get_bmi(user_data['weight'], user_data['height'])
    data = {
        'bac':  "{:.3f}".format(bac),
        'date_of_first_drink': "{d:02d}-{m:02d}-{y:04d}".format(d=now.date().day, m=now.date().month, y=now.date().year),
        'date_of_last_drink': "{d:02d}-{m:02d}-{y:04d}".format(d=then.date().day, m=then.date().month, y=then.date().year),
        'time_of_first_drink': "{h:02d}:{m:02d}".format(h=now.time().hour, m=now.time().minute),
        'time_of_last_drink': "{h:02d}:{m:02d}".format(h=then.time().hour, m=then.time().minute),
        'sobering_time': sobering_time_projection(15, gender, bac).popitem()[0],
        'max_alcohol_intake': mai_send,
        'translate_bac': translate_bac(gender, user_data['weight'], mai, classic_alcohols),
        'gender': gender,
        'weight': user_data['weight'],
        'height': user_data['height'],
        'drinks': rel_drinks,
        'bmi': bmi,
        'bmi_short': "{:.2f}".format(bmi)
    }
    return render(request, 'calculator.html', data)


def get_logs(user):
    logs = db.child('users').child(user['localId']).child('logs').get().val()
    return logs


def get_drinks(logs):
    drinks = []
    for key in logs:
        drinks.append(Alcohol(logs[key]['name'], logs[key]['volume'], logs[key]['percentage'], logs[key]['date']))
    return drinks



