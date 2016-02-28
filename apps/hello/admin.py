# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Person, RequestStore


class PersonAdmin(admin.ModelAdmin):
    pass


class RequestStoreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)
admin.site.register(RequestStore, RequestStoreAdmin)
