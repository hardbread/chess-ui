from django.conf.urls import url

from views import tournaments_all

urlpatterns = [
    url(r'^tournaments/$', tournaments_all, name='tournaments_all'),
]


