from django.conf.urls import url

from . import views

app_name = 'combine_gvcf'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
