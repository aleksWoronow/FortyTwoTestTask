# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.shortcuts import render

from .models import Person


def home_page(request):
    context = {}
    person = Person.objects.first()
    context['person'] = person
    return render(request, 'home.html', context)


def request_view(request):
    context = {
        'path': '/',
        'method': 'CET',
        'req_date': datetime.datetime.now()
        }
    return render(request, 'requests.html', context)
