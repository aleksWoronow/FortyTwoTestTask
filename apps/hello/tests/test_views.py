# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from ..views import home_page, request_view, request_ajax
from ..models import RequestStore


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


class RequestViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.get(id=1)

    def test_request_view(self):
        """Test request_view"""

        request = self.client.get(reverse('hello:requests'))
        request.user = AnonymousUser()
        response = request_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests.html')
        self.assertIn('Requests', response.content)
        self.assertIn('Path', response.content)
        self.assertIn('Method', response.content)
        self.assertIn('Date', response.content)

        # if request from anonymoususer new_request = 1
        self.client.get(reverse('hello:home'))
        all_req = RequestStore.objects.all()
        self.assertEquals(len(all_req), 1)
        only_req = all_req[0]
        self.assertEquals(only_req.path, '/')
        self.assertEquals(only_req.method, 'GET')
        self.assertEquals(only_req.new_request, 1)

        # if request from authenticated user new_request = 0
        request.user = self.user
        response = request_view(request)

        all_req = RequestStore.objects.all()
        self.assertEquals(len(all_req), 1)
        only_req = all_req[0]
        self.assertEquals(only_req.path, '/')
        self.assertEquals(only_req.method, 'GET')
        self.assertEquals(only_req.new_request, 0)


class RequestAjaxTest(TestCase):
    def test_request_ajax_view(self):

        """Test request ajax view"""
        request = self.client.get(reverse('hello:home'))
        request = self.client.get(reverse('hello:requests_ajax'),
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        def ajax(): return True
        request.is_ajax = ajax

        response = request_ajax(request)
        self.assertIn('method', response.content)
        self.assertIn('GET', response.content)
        self.assertIn('path', response.content)
        self.assertIn('/', response.content)
