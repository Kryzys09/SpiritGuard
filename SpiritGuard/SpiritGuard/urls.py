from django.contrib import admin
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.render_log_in_page),
    url(r'^postsign/', views.send_log_in_request),
    url(r'^postRegister/', views.send_register_request),
    url(r'^register/', views.render_register_page)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
