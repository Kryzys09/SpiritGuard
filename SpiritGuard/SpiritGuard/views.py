import pyrebase
from django.shortcuts import render
from requests.exceptions import HTTPError

from SpiritGuard.db.db_service import DatabaseService
from SpiritGuard.friends.mock_friends import get_mock_friends, create_random_img_url
from SpiritGuard.model.user import User

config = {
    "serviceAccount": "spiritguard-fc4df-firebase-adminsdk-cxm8z-9a1bae8908.json",
    "apiKey": "AIzaSyD8KdT5yIQgYks6F-rXdIFUvjaIOZd1S4M",
    "authDomain": "spiritguard-fc4df.firebaseapp.com",
    "databaseURL": "https://spiritguard-fc4df.firebaseio.com",
    "projectId": "spiritguard-fc4df",
    "storageBucket": "spiritguard-fc4df.appspot.com",
    "messagingSenderId": "787068540327",
    "appId": "1:787068540327:web:dbcaf54324705c8eedd282"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db_service = DatabaseService(firebase.database())


def render_log_in_page(request):
    return render(request, "logIn.html")


def send_log_in_request(request):
    email = request.POST.get('email')
    password = request.POST.get("password")
    try:
        auth.sign_in_with_email_and_password(email, password)
    except HTTPError as e:
        return render(request, "logIn.html", {"error": "Invalid credentials"})
    return render(request, "welcome.html", {"email": email, "friends": get_mock_friends()})


def render_register_page(request):
    return render(request, "register.html")


def send_register_request(request):
    if not request.method == 'POST':
        return render(request, "logIn.html", {"message": "Account created!"})
    email = request.POST.get('email')
    password = request.POST.get("password")
    password_confirmation = request.POST.get("password-confirm")
    if password != password_confirmation:
        return render(
            request,
            "register.html",
            {"error": "Passwords does not match each other"}
        )
    if len(password) < 6:
        return render(
            request,
            "register.html",
            {"error": "Password is too short"}
        )
    try:
        user = User(User.generate_id(), email, create_random_img_url())
        db_service.create_user(user)
        auth.create_user_with_email_and_password(email, password)
    except HTTPError:
        return render(request, "logIn.html", {"error": "Something went wrong"})
    return render(request, "logIn.html", {"message": "Account created!"})
