from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^calculators/$', views.render_calculator),
]
