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
    return render(request, 'requests.html')


def request_ajax(request):
    if request.is_ajax():
        context = [
            {'path': '/',
             'method': 'GET',
             'req_date': str(datetime.datetime(2005, 7, 14, 12, 30)),
             'new_req': 1},
            {'path': '/',
             'method': 'GET',
             'req_date': str(datetime.datetime(2005, 7, 14, 12, 35)),
             'new_req': 0}]
        data = json.dumps((1, context))
        return HttpResponse(data, content_type="application/json")

    return None
