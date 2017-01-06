from django.conf.urls import url

from . import views

app_name = 'hiphive'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]