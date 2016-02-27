# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse

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


def request_ajax(request):
    if request.is_ajax():
        context = {
            'path': '/',
            'method': 'GET',
            'req_date': str(datetime.datetime.now())
            }
        data = json.dumps(context)
        print data
        return HttpResponse(data, content_type="application/json")

    return None
