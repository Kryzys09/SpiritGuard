from datetime import datetime, timedelta
import pyrebase
from django.shortcuts import render, redirect
from requests.exceptions import HTTPError
from .settings import config
import plotly.graph_objects as pgo
import dateutil.parser

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

def main_page(request):
    print('USER TEST: ', request.session['user'])
    return render(request, "main-panel.html", {'user_id': request.session['user']['localId']})


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

def render_chart(request):
    user_id = request.session['user']['localId']
    users = database.child('users') \
        .get() \
        .val()
    global_chart_data = get_global_consumption_data(users)
    user_chart_data = get_user_consumption_stats(user_id, users)
    friends_chart_data = get_friends_consumption_stats(user_id, users)

    g_x, g_y = list(global_chart_data.keys()), list(global_chart_data.values())
    u_x, u_y = list(user_chart_data.keys()), list(user_chart_data.values())
    f_x, f_y = list(friends_chart_data.keys()), list(friends_chart_data.values())

    figure = pgo.Figure(
            data=[
                pgo.Scatter(x=g_x, y=g_y, name="Global"),
                pgo.Scatter(x=u_x, y=u_y, name="Current user"),
                pgo.Scatter(x=f_x, y=f_y, name="Friends")
            ]
        )
    figure.update_layout(
        title={
            "text": "Alcohol consumption in last 30 days",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
        },
        yaxis = {
            "title_text": "Alcohol in grams [g]"
        },
        height=800
    )

    figure_html = figure.to_html(full_html=False, )
    return render(request, 'showChart.html', { "global": figure_html })

def get_global_consumption_data(users_data):
    chart_data = generate_chart_data_object()
    users_logs = [
        list(user['logs'].values())
        for user in list(users_data.values()) if 'logs' in user.keys()
    ]
    for log_set in users_logs:
        summarize_alcohol_consumption(log_set, chart_data)
    return chart_data

def get_user_consumption_stats(user_id, users_data):
    chart_data = generate_chart_data_object()
    if user_id in users_data.keys():
        user_stats = users_data[user_id]
        if 'logs' in user_stats.keys():
            log_set = list(user_stats['logs'].values())
            summarize_alcohol_consumption(log_set, chart_data)
    return chart_data

def get_friends_consumption_stats(user_id, users_data):
    chart_data = generate_chart_data_object()
    friends = get_friends(user_id, users_data)
    friends_logs = get_friends_logs(friends, users_data)
    for log_set in friends_logs:
        summarize_alcohol_consumption(log_set, chart_data)
    return chart_data

def summarize_alcohol_consumption(log_set, chart_data):
    for log in log_set:
        conv_date = datetime.datetime.strptime(log['date'], "%d-%m-%Y %H:%M")
        if conv_date.date() <= datetime.datetime.today().date():
            chart_data[conv_date.date()] += log['volume'] * log['percentage']

def get_friends(user_id, users_data):
    return list(users_data[user_id]['friends'].keys()) if 'friends' in users_data[user_id].keys() else []

def get_friends_logs(friends_ids, users_data):
    return [list(users_data[friend_id]['logs'].values()) for friend_id in friends_ids]

def get_users_data():
    return database.child('users') \
        .get() \
        .val()

def generate_chart_data_object():
    return {
        datetime.datetime.today().date() - datetime.timedelta(days=i): 0 for  i in range(30)
    }
