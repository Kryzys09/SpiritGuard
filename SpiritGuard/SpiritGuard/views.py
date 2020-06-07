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
    x, y = get_drinking_global_stats()
    figure = pgo.Figure(data=[pgo.Bar(x=x, y=y), pgo.Bar(x=x, y=y)])
    figure.update_layout(title={
        "text": "Alcohol consumption in last 30 days",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    })

    figure_html = figure.to_html(full_html=False)
    return render(request, 'showChart.html', { "global": figure_html })

def get_drinking_global_stats():
    users = database.child('users') \
        .get() \
        .val()
    users = list(users.values())
    users_logs = [list(user['logs'].values()) for user in users if 'logs' in user.keys()]
    chartData = {
        datetime.today().date() - timedelta(days=i): 0 for  i in range(30)
    }
    for log_set in users_logs:
        for log in log_set:
            conv_date = datetime.strptime(log['date'], "%Y-%m-%d %H:%M:%S")
            chartData[conv_date.date()] += log['volume'] * log['percentage']

    return list(chartData.keys()), list(chartData.values())