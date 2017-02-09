from django.conf.urls import url

from . import views

app_name = 'exomewalker'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^output/(?P<output_name>\w+)', views.output, name='output'),
    url(r'export/(?P<output_name>\w+)', views.export, name='export'),
]
