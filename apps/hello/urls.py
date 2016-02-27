# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home_page, name='home'),
    url(r'^requests/$', views.request_view, name='requests'),
)
