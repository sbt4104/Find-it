from . import views
from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from case import urls
urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name =  'account/login.html'), name= 'login' ),
    url(r'^logout/$', LogoutView.as_view(template_name =  'account/logout.html'), name='logout' ),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^profile/$', views.view_profile, name = 'view_profile'),
]
