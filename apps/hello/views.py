# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.core import serializers

from .decorators import not_record_request
from .models import Person, RequestStore


def home_page(request):
    context = {}
    person = Person.objects.first()
    context['person'] = person
    return render(request, 'home.html', context)


@not_record_request
def request_view(request):
    if request.user.is_authenticated():
        RequestStore.objects.filter(new_request=1).update(new_request=0)
    return render(request, 'requests.html')


@not_record_request
def request_ajax(request):
    if request.is_ajax():
        new_request = RequestStore.objects.filter(new_request=1).count()
        request_list = RequestStore.objects.all()[:10]
        list = serializers.serialize("json", request_list)
        data = json.dumps((new_request, list))
        return HttpResponse(data, content_type="application/json")

    return HttpResponseBadRequest('Error request')
