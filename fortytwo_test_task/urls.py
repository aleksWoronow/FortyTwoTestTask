# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^', include('apps.hello.urls', namespace='hello')),

    url(r'^admin/', include(admin.site.urls)),
)
