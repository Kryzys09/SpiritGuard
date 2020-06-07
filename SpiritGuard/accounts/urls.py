from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^pre_login/$', views.render_log_in_page),
    url(r'^pre_login/postsign/', views.send_log_in_request),
    url(r'^pre_login/postRegister/', views.send_register_request),
    url(r'^pre_login/register/', views.render_register_page),
    url(r'^pre_login/register_next/', views.register_new_user),
    url(r'^settings/', views.render_edit_account_details),
    url(r'^register_next/', views.register_new_user),
    url(r'^profile', views.load_profile),
    url(r'^friends/$', views.load_friends),
    url(r'^add_friend', views.add_friend),
    url(r'^search_users/', views.get_users_list)
]
