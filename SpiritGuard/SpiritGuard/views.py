import datetime
import pyrebase
from django.shortcuts import render, redirect
from requests.exceptions import HTTPError
from .settings import config

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

def main_page(request):
    return render(request, "main-panel.html")


def log_out(request):
    request.session.clear()
    print('CACHE CLEARED')
    return redirect('/accounts/pre_login/')


def addAlcohol(request):
    now = datetime.datetime.now() + datetime.timedelta(hours=2)
    date = "{d:02d}-{m:02d}-{y:04d}".format(d=now.date().day, m=now.date().month, y=now.date().year)
    time = "{h:02d}:{m:02d}".format(h=now.time().hour, m=now.time().minute)

    data = {
        'date': date,
        'time': time
    }
    return render(request, "addAlcohol.html", data)


def post_create(request):
    name = request.POST.get('name-input')
    volume = request.POST.get('volume-input')
    percentage = request.POST.get('percentage-input')
    date = request.POST.get('date-input')
    time = request.POST.get('time-input')
    data={
        'name':name,
        'volume': int(volume),
        'percentage': float(percentage),
        'date': date + ' ' + time
    }
    idtoken = request.session['user']['localId']
    database.child('users').child(idtoken).child('logs').push(data)

    return render(request, "addAlcohol.html")


def post_add_wine(request):
    now = datetime.datetime.now() + datetime.timedelta(hours=2)
    date = "{d:02d}-{m:02d}-{y:04d}".format(d=now.date().day, m=now.date().month, y=now.date().year)
    time = "{h:02d}:{m:02d}".format(h=now.time().hour, m=now.time().minute)
    data = {
        'name': 'wine',
        'volume': 150,
        'percentage': 0.116,
        'date': date + ' ' + time
    }
    idtoken = request.session['user']['localId']
    database.child('users').child(idtoken).child('logs').push(data)
    return render(request, "main-panel.html")
def post_add_beer(request):
    now = datetime.datetime.now() + datetime.timedelta(hours=2)
    date = "{d:02d}-{m:02d}-{y:04d}".format(d=now.date().day, m=now.date().month, y=now.date().year)
    time = "{h:02d}:{m:02d}".format(h=now.time().hour, m=now.time().minute)
    data = {
        'name': 'beer',
        'volume': 500,
        'percentage': 0.05,
        'date': date + ' ' + time
    }
    idtoken = request.session['user']['localId']
    database.child('users').child(idtoken).child('logs').push(data)
    return render(request, "main-panel.html")
def post_add_vodka(request):

    now = datetime.datetime.now() + datetime.timedelta(hours=2)
    date = "{d:02d}-{m:02d}-{y:04d}".format(d=now.date().day, m=now.date().month, y=now.date().year)
    time = "{h:02d}:{m:02d}".format(h=now.time().hour, m=now.time().minute)
    data = {
        'name': 'vodka',
        'volume': 30,
        'percentage': 0.40,
        'date': date + ' ' + time
    }
    idtoken = request.session['user']['localId']
    database.child('users').child(idtoken).child('logs').push(data)
    return render(request, "main-panel.html")