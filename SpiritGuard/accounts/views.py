import pyrebase
from django.shortcuts import render, redirect
from requests.exceptions import HTTPError
from SpiritGuard.settings import config


firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()


def render_log_in_page(request):
    return render(request, "logIn.html")


def send_log_in_request(request):
    email = request.POST.get('email')
    password = request.POST.get("password")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except HTTPError as e:
        print('ERROR: ', e)
        return render(request, "logIn.html", {"error": "Invalid credentials"})
    request.session['user'] = user
    print('USERTEST: ', request.session['user'])
    return redirect('/')


def render_register_page(request):
    return render(request, "register.html")


def send_register_request(request):
    email = request.POST.get('email')
    password = request.POST.get("password")
    password_confirmation = request.POST.get("password-confirm")
    if password != password_confirmation:
        return render(
            request,
            "register.html",
            {"error": "Passwords do not match"}
        )
    if len(password) < 6:
        return render(
            request,
            "register.html",
            {"error": "Password is too short"}
        )
    try:
        user = auth.create_user_with_email_and_password(email, password)
    except HTTPError:
        return render(request, "logIn.html", { "error": "Something went wrong"})
    new_user(user)
    return render(request, "logIn.html", {"message": "Account created!"})


def new_user(user):
    token = user['idToken']
    id = user['localId']
    data = {
        'email': user['email'],
        'image': ""
    }
    db.child("users").child(id).set(data, token)
