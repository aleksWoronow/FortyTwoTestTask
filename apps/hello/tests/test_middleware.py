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

    def test_middleware(self):
        """Test middleware RequestMiddle."""
        request = self.factory.get(reverse('hello:home'))

        # middleware don't store request to decorated function
        decorated_func = not_record_request(home_page)
        request.user = self.user
        self.middleware.process_view(request,  decorated_func)
        rs = RequestStore.objects.all()
        self.assertQuerysetEqual(rs, [])

        # middleware store request to undecorated function
        request.user = self.user
        self.middleware.process_view(request, home_page)
        rs = self.request_store.objects.all()
        self.assertEquals(len(rs), 1)
        only_one_rs = rs[0]
        self.assertEqual(only_one_rs.path, reverse('hello:home'))

        # if user is anonymous
        request.user = AnonymousUser()
        self.middleware.process_view(request, home_page)
        rs = self.request_store.objects.all()
        self.assertEquals(len(rs), 2)
        only_one_rs = rs[1]
        self.assertEqual(only_one_rs.path, reverse('hello:home'))
