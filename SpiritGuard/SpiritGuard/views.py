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



def render_edit_account_details(request):
    return render(request, "editAccountDetails.html")

def submit_that_shit_bwooy(request):
    requestData = request.POST
    print(requestData)
    print(request.FILES)
    data = {
        "name": requestData.get("name"),
        "surname": requestData.get("surname"),
        "birth_date": datetime.datetime.strptime(
            requestData.get("date_of_birth"), "%d.%m.%Y"
        ),
        "weight": requestData.get("weight"),
        "height": requestData.get("height"),
        "gender": requestData.get("gender")
    }
    print(data)
    return render(request, "welcome.html")