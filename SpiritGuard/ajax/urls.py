from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^users/$', views.get_users, name='get_users')
]
