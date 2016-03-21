
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls', namespace='core')),
    url(r'^conta/', include('accounts.urls', namespace='accounts'))
]
