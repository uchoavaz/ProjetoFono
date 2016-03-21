
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^perfil$', views.profile, name='profile'),
    url(r'^alterar-senha$', views.password, name='password')
]
