# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.http import HttpRequest

from ..views import home_page


class HomePageViewTest(TestCase):

    def test_home_page_view(self):
        """Test view home_page"""
        request = self.client.get(reverse('hello:home'))
        response = home_page(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('Aleks', response.content)
        self.assertIn('Woronow', response.content)
        self.assertIn('Feb. 25, 2016', response.content)
        self.assertIn('aleks.woronow@yandex.ru', response.content)
        self.assertIn('aleks_woronow', response.content)
        self.assertIn('aleksw@42cc.co', response.content)
        self.assertIn('I was born ...', response.content)


class HomePageTest(TestCase):
    def test_home_page(self):
        """Test home page"""

        response = self.client.get(reverse('hello:home'))

        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response,
                            '<h1>42 Coffee Cups Test Assignment</h1>',
                            html=True)
        self.assertContains(response, 'Aleks')
        self.assertContains(response, 'Woronow')
        self.assertContains(response, 'Feb. 25, 2016')
        self.assertContains(response, 'aleks.woronow@yandex.ru')
        self.assertContains(response, 'aleksw@42cc.co')
        self.assertContains(response, 'aleks_woronow')
        self.assertContains(response, 'I was born ...')

    def test_home_page_returns_correct_html(self):
        """Test home page returns correct html"""
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.strip().
                        startswith(b'<!DOCTYPE html>'))
        self.assertIn(b'<title>My card</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
