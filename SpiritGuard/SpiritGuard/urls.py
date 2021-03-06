from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.main_page),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^alcohols/', include('alcohols.urls')),
    url(r'^ajax/', include('ajax.urls')),
    url(r'^logout/', views.log_out),
    url(r'^addAlcohol/', views.addAlcohol),
    url(r'^post_create/', views.post_create),
    url(r'^post_add_beer/', views.post_add_beer),
    url(r'^post_add_wine/', views.post_add_wine),
    url(r'^post_add_vodka/', views.post_add_vodka),
    url(r'^stats/', views.render_chart),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
