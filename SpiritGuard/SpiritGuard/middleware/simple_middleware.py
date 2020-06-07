from django.shortcuts import redirect

def simple_middleware(get_response):
    def middleware(request):
        print(request)
        if 'user' in request.session:
            request.session.set_expiry(600)
            print('USER: ', request.session['user'])
            if request.path.startswith('/accounts/pre_login/'):
                response = redirect('/')
            else:
                response = get_response(request)
        else:
            if request.path.startswith('/accounts/pre_login/'):
                response = get_response(request)
            else:
                response = redirect('/accounts/pre_login/')
        return response
    return middleware
