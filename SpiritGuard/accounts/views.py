from datetime import datetime, date
import pyrebase
from django.shortcuts import render, redirect
from requests.exceptions import HTTPError
from SpiritGuard.settings import config
from django.core.files.storage import FileSystemStorage

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
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
    return render(
        request,
        "editAccountDetails.html",
        { "email": email, "password": password }
    )

def render_edit_account_details(request):
    user_data = {}
    user = request.session['user']
    storage.child('images/' + user['localId'] + '.jpg').download('static/gfx/avatar.jpg')
    if 'user' in request.session.keys():
        user = request.session['user']
        user_data = db.child('users') \
            .child(user['localId']) \
            .get() \
            .val()
        user_data = dict(user_data)

    return render(request, "editAccountDetails.html", user_data)


def register_new_user(request):
    try:
        birth_date = datetime.strptime(
                request.POST.get("date_of_birth"),
                "%Y-%m-%d"
            )
        email = request.POST.get('email')
        password = request.POST.get("password")

        if not is_birth_date_ok(birth_date):
            return render(
                request,
                "editAccountDetails.html",
                { "error": "Za młody jesteś byczq" }
            )
        
        if 'user' in request.session.keys():
            user = request.session['user']
        else:
            user = auth.create_user_with_email_and_password(email, password)
        if 'avatar' not in request.FILES.keys():
            file_path = 'default2.png'
        else:
            file_path = handle_file(request.FILES['avatar'], user)

        data = generate_user_data_object(request.POST, birth_date)
        if data['gender'] == "":
            raise ValueError()
        data['email'] = email
        data['avatar'] = file_path
        db.child('users') \
            .child(user['localId']) \
            .update(data, user['idToken'])
             
    except ValueError:
        return render(
            request,
            "editAccountDetails.html",
            { "error": "Oj nie byczq -1" }
        )
    except (HTTPError, KeyError):
        return render(request, "logIn.html", { "error": "Something went wrong"})
    
    return redirect("/")


def is_birth_date_ok(birth_date: datetime) -> bool:
    now = date.today()
    first_good_date = datetime(now.year - 18, now.month, now.day)
    return birth_date <= first_good_date


def generate_user_data_object(request_data, birth_date):
    return {
        "nickname": request_data.get("nickname"),
        "birth_date": str(birth_date),
        "weight": float(request_data.get("weight")),
        "height": float(request_data.get("height")),
        "gender": request_data.get("gender")
    }


def handle_file(file, user):
    file_name = user['localId'] + '.jpg'
    storage.child('images/' + file_name).put(file)
    return file_name