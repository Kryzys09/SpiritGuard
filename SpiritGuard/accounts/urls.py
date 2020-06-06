from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.render_log_in_page),
    url(r'^postsign/', views.send_log_in_request),
    url(r'^postRegister/', views.send_register_request),
    url(r'^register/', views.render_register_page),
    url(r'^edit_account_details/', views.render_edit_account_details),
    url(r'^register_next/', views.register_new_user),
]
