# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from django.contrib import admin

from hello.forms import LoginForm


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^', include('apps.hello.urls', namespace='hello')),
    url(r'^login/$',
        auth_views.login,
        {'authentication_form': LoginForm},
        name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),  

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
