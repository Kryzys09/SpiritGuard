import pyrebase
from django.http import JsonResponse

from SpiritGuard.settings import config

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()


def get_users(request):
    users = db.child('users').get().val()
    searched_nickname = request.GET.get('nickname', None)
    users_list = []
    for local_id in users:
        u = users[local_id]
        users_list.append(u)
    data = {'users': users_list}
    return JsonResponse(data)
