from django.conf.urls import url

from . import views

app_name = 'exomewalker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^output/(?P<output_name>\w+)', views.output, name='output'),
]
