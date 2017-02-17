from django.conf.urls import url

from . import views

app_name = 'common_novel'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
