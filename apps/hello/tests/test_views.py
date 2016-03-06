# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
import StringIO

from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..views import home_page, request_view, request_ajax
from ..models import Person, RequestStore
from .test_models import get_temporary_image


# create text file for test
def get_temporary_text_file(name):
    io = StringIO.StringIO()
    io.write('test')
    text_file = InMemoryUploadedFile(
        io, None, name, 'text', io.len, None)
    text_file.seek(0)
    return text_file


class HomePageViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_home_page_view(self):
        """Test view home_page"""
        # Create an instance of a GET request.
        request = self.factory.get('/')

        # Test home_page() as if it were deployed at /
        response = home_page(request)
        self.assertEqual(response.status_code, 200)

        # Test home.html was used in rendering response
        self.assertTemplateUsed(response, 'home.html')


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

    def test_home_page_if_person_more_then_one(self):
        """
        Test check that home page displays only the first record
        that db has more than 1 instance
        """
        # Create second person
        Person.objects.create(
            name='Ivan',
            surname='Ivanov',
            email='ivan@yandex.ru',
            jabber='ivan@42cc.co',
            skype_id='ivan_ivanov',
            date_of_birth=date(2016, 1, 25),
            bio='I was born ...')

        # Check that two person in db
        all_persons = Person.objects.all()
        self.assertEquals(len(all_persons), 2)
        first_person = all_persons[0]

        # home page displays only the first record: Aleks
        response = self.client.get(reverse('hello:home'))
        self.assertEquals(response.context['person'], first_person)
        self.assertContains(response, 'Woronow')
        self.assertNotContains(response, 'Ivan')

    def test_home_page_if_no_person(self):
        """
        Test check that home page displays "Contact data no yet"
        if db has not person instance
        """
        # Delete all the Person instance
        Person.objects.all().delete()

        # home page displays "Contact data no yet"
        response = self.client.get(reverse('hello:home'))
        self.assertEquals(response.context['person'], None)
        self.assertContains(response, 'Contact data no yet')

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
        self.factory = RequestFactory()
        self.user = get_user_model().objects.get(id=1)

    def test_request_view(self):
        """Test request_view"""

        request = self.factory.get(reverse('hello:requests'))
        request.user = AnonymousUser()
        response = request_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests.html')
        self.assertIn('Requests', response.content)
        self.assertIn('Path', response.content)
        self.assertIn('Method', response.content)
        self.assertIn('Date', response.content)

    def test_request_view_visit_anonymoususer(self):
        """
        Test check request_view return RequestStore instances
        that have new_request = 1 if request from anonymoususer
        """
        self.client.get(reverse('hello:home'))
        request = self.factory.get(reverse('hello:requests'))
        request.user = AnonymousUser()
        request_view(request)

        # now new_request = 1
        all_req = RequestStore.objects.all()
        self.assertEquals(len(all_req), 1)
        only_req = all_req[0]
        self.assertEquals(only_req.path, '/')
        self.assertEquals(only_req.method, 'GET')
        self.assertEquals(only_req.new_request, 1)

    def test_request_view_visit_authenticated_user(self):
        """
        Test check request_view return RequestStore instances
        that have new_request = 0 if request from authenticated user
        """
        self.client.get(reverse('hello:home'))
        request = self.factory.get(reverse('hello:requests'))
        request.user = self.user
        request_view(request)

        # now new_request = 0
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


class FormPageTest(TestCase):
    def setUp(self):
        self.person = Person.objects.first()
        self.data = dict(name='Ivan', surname='Ivanov',
                         date_of_birth='2016-02-02',
                         bio='', email='ivanov@yandex.ru',
                         jabber='iv@jabb.com',
                         image=get_temporary_image())

    def test_form_page_view(self):
        """
        Test check access to form page only authenticate
        users and it used template request.html.
        """

        # if user is not authenticate
        response = self.client.get(reverse('hello:form'))
        self.assertEqual(response.status_code, 302)

        # after authentication
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('hello:form'))
        self.assertTemplateUsed(response, 'person_form.html')

    def test_form_page_edit_data(self):
        """Test check edit data at form page."""

        # login on the site
        self.client.login(username='admin', password='admin')

        # send new data to server
        response = self.client.post(reverse('hello:form'), self.data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.get(reverse('hello:form'))
        self.assertEqual(response.status_code, 200)

        # data are shown at form page according to changed data
        self.assertNotIn(self.person.name, response.content)
        self.assertNotIn(self.person.surname, response.content)
        self.assertNotIn(self.person.date_of_birth.strftime('%Y-%m-%d'),
                         response.content)
        self.assertNotIn(self.person.email, response.content)
        self.assertNotIn(self.person.jabber, response.content)

        self.assertIn('Ivan', response.content)
        self.assertIn('Ivanov', response.content)
        self.assertIn('2016-02-02', response.content)
        self.assertIn('ivanov@yandex.ru', response.content)
        self.assertIn('iv@jabb.com', response.content)
        self.assertIn('test.jpg', response.content)

    def test_form_page_on_text_file(self):
        """
        Test check form_page return error if upload text file.
        """

        # add to data text file text.txt
        self.data.update({'image': get_temporary_text_file('text.txt')})

        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('hello:form'), self.data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(400, response.status_code)
        self.assertIn('Upload a valid image. The file you uploaded',
                      response.content)

        # add to data text file text.jpg
        self.data.update({'image': get_temporary_text_file('text.jpg')})

        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('hello:form'), self.data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(400, response.status_code)
        self.assertIn('Upload a valid image. The file you uploaded',
                      response.content)

    def test_form_page_edit_data_to_wrong(self):
        """Test check edit data at form page to wrong data."""

        # check enter empty name and invalid data_of_birth, email
        # login on the site
        self.client.login(username='admin', password='admin')

        # edit data with empty name and invalid data_of_birth, email
        self.data.update({'name': '',
                          'date_of_birth': 'date',
                          'email': 'ivanovyandex.ru'})

        # send new data to server
        response = self.client.post(reverse('hello:form'), self.data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)

        # response errors
        self.assertIn('This field is required.', response.content)
        self.assertIn('Enter a valid date.', response.content)
        self.assertIn('Enter a valid email address.', response.content)

        # data in db did not change
        edit_person = Person.objects.first()
        self.assertEqual(self.person.name, edit_person.name)
