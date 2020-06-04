import pyrebase
from django.shortcuts import render, redirect
from requests.exceptions import HTTPError
from .settings import config
# Tymczasowo - docelowo wyrzucić do innego pliku

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def main_page(request):
    return render(request, "main-panel.html")


def log_out(request):
    request.session.clear()
    print('CACHE CLEARED')
    return redirect('/accounts/')
