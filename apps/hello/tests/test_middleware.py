# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from apps.middleware.helloRequest import RequestMiddle
from ..models import RequestStore
from ..decorators import not_record_request
from ..views import home_page


class RequestMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestMiddle()
        self.request_store = RequestStore
        self.user = get_user_model().objects.get(id=1)

    def test_middleware_is_included(self):
        """Test for inclusion RequestMiddleware in project"""
        self.client.get(reverse('hello:home'))
        last_middleware_obj = self.request_store.objects.last()
        self.assertEqual(last_middleware_obj.method, 'GET')
        self.assertEqual(last_middleware_obj.path, reverse('hello:home'))

    def test_middleware_not_store_request_decorated_func(self):
        """
        Test middleware RequestMiddle don't store request
        to decorated function.
        """
        request = self.factory.get(reverse('hello:home'))

        # decorated function
        decorated_func = not_record_request(home_page)
        request.user = self.user

        # request don't store
        self.middleware.process_view(request,  decorated_func)
        rs = RequestStore.objects.all()
        self.assertQuerysetEqual(rs, [])

    def test_middleware_store_request_undecorated_func(self):
        """
        Test middleware RequestMiddle store request
        undecorated function.
        """
        request = self.factory.get(reverse('hello:home'))

        # middleware store request to undecorated function
        request.user = self.user
        self.middleware.process_view(request, home_page)
        rs = self.request_store.objects.all()
        self.assertEquals(len(rs), 1)
        only_one_rs = rs[0]
        self.assertEqual(only_one_rs.path, reverse('hello:home'))

    def test_middleware_store_request_anonymoususer(self):
        """
        Test middleware RequestMiddle store request anonymoususer.
        """
        request = self.factory.get(reverse('hello:home'))

        # set user is anonymous
        request.user = AnonymousUser()

        # middleware store request
        self.middleware.process_view(request, home_page)
        rs = self.request_store.objects.all()
        self.assertEquals(len(rs), 1)
        only_one_rs = rs[0]
        self.assertEqual(only_one_rs.path, reverse('hello:home'))

    def test_midleware_set_priority_new_request(self):
        """
        Test middleware RequestMiddle set the priority of a new request,
        same as analoging requests.
        """
        request = self.factory.get(reverse('hello:home'))

        # middleware store request with default priority = 0
        request.user = self.user
        self.middleware.process_view(request, home_page)
        rs = self.request_store.objects.all()
        self.assertEquals(len(rs), 1)
        only_one_rs = rs[0]
        self.assertEqual(only_one_rs.priority, 0)

        # change priority to 1
        req_home = self.request_store.objects.get(path=reverse('hello:home'))
        req_home.priority = 1
        req_home.save()

        request = self.factory.post(reverse('hello:home'))

        # now middleware store request with priority = 1
        request.user = self.user
        self.middleware.process_view(request, home_page)
        req_home_post = self.request_store.objects.get(method='POST')
        self.assertEqual(req_home_post.priority, 1)
