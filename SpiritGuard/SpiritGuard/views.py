import pyrebase
from django.shortcuts import render, redirect
from requests.exceptions import HTTPError
from .settings import config
import plotly.graph_objects as pgo
from datetime import datetime, timedelta

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

def main_page(request):
    return render(request, "main-panel.html")


def log_out(request):
    request.session.clear()
    print('CACHE CLEARED')
    return redirect('/accounts/')



def newpage(request):

    alcohols = database.child("alcohols").shallow().get().val()
    alcohols_list = []
    for i in alcohols:
        alcohols_list.append(i)

    alcohols_list.sort(reverse = False)



    return render(request, "newpagee.html",{'alcohols_list':alcohols_list})

def post_create(request):
    work = request.POST.get('work')
    data={
        'work':work
    }
    print('WORK: ', work)
    database.child('users').push(data)

    return render(request,"newpagee.html")

def render_chart(request):
    user_id = request.session['user']['localId']
    users = database.child('users') \
        .get() \
        .val()
    global_chart_data = get_global_consumption_data(users)
    user_chart_data = get_user_consumption_stats(user_id, users)
    g_x, g_y = list(global_chart_data.keys()), list(global_chart_data.values())
    u_x, u_y = list(user_chart_data.keys()), list(user_chart_data.values())
    figure = pgo.Figure(
            data=[
                pgo.Bar(x=g_x, y=g_y, name="Global"),
                pgo.Bar(x=u_x, y=u_y, name="Current user")
            ]
        )
    figure.update_layout(
        title={
            "text": "Alcohol consumption in last 30 days",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    figure_html = figure.to_html(full_html=False)
    return render(request, 'showChart.html', { "global": figure_html })

def get_global_consumption_data(users_data):
    chart_data = generate_chart_data_object()
    users_logs = [
        list(user['logs'].values())
        for user in list(users_data.values()) if 'logs' in user.keys()
    ]
    for log_set in users_logs:
        for log in log_set:
            conv_date = datetime.strptime(log['date'], "%Y-%m-%d %H:%M:%S")
            chart_data[conv_date.date()] += log['volume'] * log['percentage']
    return chart_data

def get_user_consumption_stats(user_id, users_data):
    chart_data = generate_chart_data_object()
    if user_id in users_data.keys():
        user_stats = users_data[user_id]
    else:
        return chart_data
    if 'logs' in user_stats.keys():
        user_logs = list(user_stats['logs'].values())
    else:
        return chart_data

    for log in user_logs:
        conv_date = datetime.strptime(log['date'], "%Y-%m-%d %H:%M:%S")
        chart_data[conv_date.date()] += log['volume'] * log['percentage']

    return chart_data

def get_users_data():
    return database.child('users') \
        .get() \
        .val()

def generate_chart_data_object():
    return {
        datetime.today().date() - timedelta(days=i): 0 for  i in range(30)
    }