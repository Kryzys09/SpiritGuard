import pyrebase
from django.shortcuts import render, redirect
from requests.exceptions import HTTPError
<<<<<<< HEAD
from .settings import config
# Tymczasowo - docelowo wyrzucić do innego pliku

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

<<<<<<< HEAD
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
