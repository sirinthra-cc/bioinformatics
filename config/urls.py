"""bioinformatics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', include('filter.urls')),
    url(r'^common-variant/', include('common_variant.urls')),
    url(r'^de-novo/', include('de_novo.urls')),
    url(r'^hiphive/', include('hiphive.urls')),
    url(r'^exomewalker/', include('exomewalker.urls')),
    url(r'^common-novel/', include('common_novel.urls')),
    url(r'^filter/', include('filter.urls')),
    url(r'^admin/', admin.site.urls),
]
