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
    try:
        birth_date = datetime.datetime.strptime(
                request.POST.get("date_of_birth"),
                "%d.%m.%Y"
            )

        if is_birth_date_ok(birth_date):     
            data = generate_user_data_object(request.POST, birth_date)
            user = request.session['user']
            database.child('users') \
                .child(user['localId']) \
                .update(data, user['idToken'])
        else:
            return render(
                request,
                "editAccountDetails.html",
                { "error": "Za młody jesteś mordo" }
            ) 
    except ValueError:
        return render(
            request,
            "editAccountDetails.html",
            { "error": "Oj nie byczq -1" }
        )

    return redirect("/")

def is_birth_date_ok(birth_date: datetime.datetime) -> bool:
    now = datetime.date.today()
    first_good_date = datetime.datetime(now.year - 18, now.month, now.day)
    return birth_date <= first_good_date

def generate_user_data_object(request_data, birth_date):
    return {
        "nickname": request_data.get("nickname"),
        "birth_date": str(birth_date),
        "weight": float(request_data.get("weight")),
        "height": float(request_data.get("height")),
        "gender": request_data.get("gender")
    }