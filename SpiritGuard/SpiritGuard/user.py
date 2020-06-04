
class User:
    def __init__(self, db, user):
        self.email = user.email
        self.username = user.username
        self.password = user.password

        data = {
            'email': user.email,
            'username': user.username,
            'password': user.password
        }
        db.child('users').push(data)