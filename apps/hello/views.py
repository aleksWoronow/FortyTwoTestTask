# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.shortcuts import render


def home_page(request):
    context = {
        'name': 'Aleks',
        'surname': 'Woronow',
        'date_of_birth': date(2016, 2, 25),
        'bio': 'I was born ...',
        'email': 'aleks.woronow@yandex.ru',
        'jabber': 'aleksw@42cc.co',
        'skype_id': 'aleks_woronow',
        'other': '...'
        }
    return render(request, 'home.html', context)
