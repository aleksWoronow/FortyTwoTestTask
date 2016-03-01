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
                     'date_of_birth': date(2105, 7, 14),
                     'email': 'aleks.woronow@ya',
                     'jabber': '42cc@khavr.com'}
        form = PersonForm(data=form_data)

        self.assertEqual(form.is_valid(), False)
        self.assertFormError('name', ['This field is required.'])
        self.assertFormError('surname', ['This field is required.'])
        self.assertFormError('date_of_birth', ['This field is required.'])
        self.assertFormError('email', ['Enter a valid email address.'])

        form_data['name'] = 'Aleks'
        form_data['surname'] = 'Woronow'
        form_data['email'] = 'aleks.woronow@yandex.ru'
        form = PersonForm(data=form_data)

        self.assertEqual(form.is_valid(), True)
