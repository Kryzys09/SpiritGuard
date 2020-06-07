from django.shortcuts import redirect

def simple_middleware(get_response):
    def middleware(request):
        print(request)
        response = get_response(request)
        # if 'user' in request.session:
        #     print('USER: ', request.session['user'])
        #     if request.path.startswith('/accounts/'):
        #         response = redirect('/')
        #     else:
        #         response = get_response(request)
        # else:
        #     if request.path.startswith('/accounts/'):
        #         response = get_response(request)
        #     else:
        #         response = redirect('/accounts/')
        return response
    return middleware
