from django.conf.urls import url

from . import views

app_name = 'de_novo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
