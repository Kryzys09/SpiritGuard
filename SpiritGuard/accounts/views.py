from datetime import datetime, date
from .friends import Friend
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
    request.session.set_expiry(900)
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
        { "email": email, "password": password, "link": '/accounts/pre_login/register_next/'}
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
        user_data['link'] = '/accounts/register_next/'
        user_data['avatar'] = db.child('users').child(user['localId']).child('avatar').get().val()

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
            file_path = ''
        else:
            file_path = handle_file(request.FILES['avatar'], user)

        data = generate_user_data_object(request.POST, birth_date)
        if data['gender'] == "":
            raise ValueError()
        data['email'] = email
        if len(file_path) > 0:
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
    url = storage.child('images/' + file_name).get_url(user['idToken'])
    return url

def load_friends(request):
    user = request.session['user']
    dict_friends = db.child('users').child(user['localId']).child('friends').get().val().keys()
    friends = []

    for friend_id in dict_friends:
        friend = db.child('users').child(friend_id).get().val()
        print(friend)
        if 'logs' in friend:
            logs = friend['logs']
        else:
            logs = []
        if 'avatar' in friend:
            avatar = friend['avatar']
        else:
            avatar = 'SpiritGuard/static/gfx/avatars/default2.png'
        friends.append(Friend(friend_id, friend['nickname'], friend['birth_date'], avatar, logs))

    data = {
        'friends': friends
    }

    return render(request, 'friends/friends.html', data)


def load_profile(request):
    local_id = request.GET['id']
    user_db = db.child('users').child(local_id).get().val()
    if 'logs' in user_db:
        logs = user_db['logs']
    else:
        logs = []
    if 'avatar' in user_db:
        avatar = user_db['avatar']
    else:
        avatar = 'SpiritGuard/static/gfx/avatars/default2.png'
    user = Friend(local_id, user_db['nickname'], user_db['birth_date'], avatar, logs)
    data = {
        'name': user.name,
        'age': user.age,
        'avatar': user.image,
        'logs': user.logs
    }
    return render(request, 'accounts/profile.html', data)
