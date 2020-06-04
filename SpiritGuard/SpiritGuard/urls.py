from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^logout/', views.log_out),
    url(r'^$', views.main_page),
    url(r'^newpage/', views.newpage),
    url(r'^post_create/', views.post_create),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
