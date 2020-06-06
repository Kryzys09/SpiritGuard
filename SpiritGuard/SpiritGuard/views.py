import pyrebase
import re
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

def get_users_list(request):
    query = request.POST['usersQuery']
    users = database \
        .child('users') \
        .get() \
        .val()
    users = [
        {
            "nickname": safe_get(user[1], 'nickname', ''),
            "avatar": safe_get(user[1], 'avatar', 'default2.png')
        } for user in users.items() if safe_get(user[1], 'nickname', '')
    ]
    users = [user for user in users if re.search(query, user['nickname'])]
    return render(request, 'search-user-result.html', { "users": users })

def safe_get(entry, field, default_val):
    return entry[field] if field in entry.keys() else default_val