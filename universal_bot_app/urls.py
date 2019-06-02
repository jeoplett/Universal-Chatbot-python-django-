# coding: utf8

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<bot_api_token>.+)/$', views.index, name='index')
]