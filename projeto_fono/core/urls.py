
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', 'core.views.login', name='login'),
    url(r'^logout$', 'core.views.logout', name='logout'),
    url(r'^$', views.home, name='home')
]