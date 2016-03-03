# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from datetime import date

from ..forms import PersonForm


class FormTest(TestCase):
    def test_form(self):
        """Test form"""
        form_data = {'name': '',
                     'surname': '',
                     'date_of_birth': 'data',
                     'email': 'aleks.woronow@ya',
                     'jabber': '42cc@khavr.com'}
        form = PersonForm(data=form_data)

        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['surname'], ['This field is required.'])
        self.assertEqual(form.errors['date_of_birth'], ['Enter a valid date.'])
        self.assertEqual(form.errors['email'],
                         ['Enter a valid email address.'])

        form_data['name'] = 'Aleks'
        form_data['surname'] = 'Woronow'
        form_data['date_of_birth'] = date(2016, 2, 29)
        form_data['email'] = 'aleks.woronow@yandex.ru'
        form = PersonForm(data=form_data)

        self.assertEqual(form.is_valid(), True)
