# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home_page, name='home'),
    url(r'^requests/$',
        TemplateView.as_view(template_name="requests.html"),
        name='requests'),
)
