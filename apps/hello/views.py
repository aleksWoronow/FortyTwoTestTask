# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .decorators import not_record_request
from .models import Person, RequestStore
from .forms import PersonForm


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


@login_required
def form_page(request):
    person = Person.objects.first()

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)

        if form.is_valid():
            new_person = form.save(commit=False)

            if request.POST.get('image-clear') is None:
                if new_person.image is None:
                    new_person.image = person.image

            new_person.save()

            if request.is_ajax():
                if getattr(settings, 'DEBUG', False):
                    time.sleep(3)

                list_pers = serializers.serialize("json", [person, ])
                return HttpResponse(json.dumps(list_pers),
                                    content_type="application/json")
            else:
                return redirect('hello:success')
        else:
            if request.is_ajax():
                if getattr(settings, 'DEBUG', False):
                    time.sleep(2)
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = unicode(e)

                return HttpResponseBadRequest(json.dumps(errors_dict),
                                              content_type="application/json")
    else:
        form = PersonForm(instance=person)

    return render(request, 'person_form.html', {'form': form})
