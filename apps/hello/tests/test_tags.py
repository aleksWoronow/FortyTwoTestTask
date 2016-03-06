# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission

from ..templatetags.edit_link import edit_link
from ..models import Person


class TagAdminLinkTest(TestCase):
    def test_edit_link_tag_is_at_home_page(self):
        """
        Test check tag is on home page
        """
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('hello:home'))
        self.assertIn(
            '<a href="/admin/hello/person/1/">(admin)</a>', response.content)

    def test_edit_link_tag_recive_model_that_register_admin(self):
        """
        Test check tag if it recive model that register in admin
        """
        # test edit_link recive instance model that register admin
        person = Person.objects.first()
        link_person_one = edit_link(person)['edit_link']

        self.client.login(username='admin', password='admin')
        response = self.client.get(link_person_one)

        self.assertIn('Django administration', response.content)
        self.assertIn(str(person), response.content)

    def test_edit_link_tag_recive_model_that_not_register_admin(self):
        """
        Test check tag if it recive model that not register in admin
        """
        # test edit_link recive instance model that not register admin
        permission = Permission.objects.first()
        link_permission_one = edit_link(permission)['edit_link']

        self.client.login(username='admin', password='admin')
        response = self.client.get(link_permission_one)
        self.assertEqual(
            '/admin/auth/permission/1/',
            link_permission_one)
        self.assertIn(
            'The page you are looking for could not be found',
            response.content)

    def test_edit_link_tag_recive_arg_that_not_instance_model(self):
        """
        Test check tag if it recive argument that not models.Model instance
        """
        # test edit_link recive invalid argument
        with self.assertRaises(TypeError) as err:
            edit_link(1)

        # now edit_link raise TypeError
        self.assertEquals(
            err.exception.args[0],
            'Invalide type arg for edit_link, shoud be models.Model instance')
