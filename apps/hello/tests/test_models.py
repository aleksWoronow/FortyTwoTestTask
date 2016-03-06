# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from PIL import Image as Img
import StringIO

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..models import Person, RequestStore, NoteModel


# create image file for test
def get_temporary_image():
        output = StringIO.StringIO()
        size = (1200, 700)
        color = (255, 0, 0, 0)
        image = Img.new("RGBA", size, color)
        image.save(output, format='JPEG')
        image_file = InMemoryUploadedFile(
            output, None, 'test.jpg', 'jpeg', output.len, None)
        image_file.seek(0)
        return image_file


class PersonModelTests(TestCase):
    def test_person_model_blank_fields_validation(self):
        """
        Test check validation blank fields person model
        """
        person = Person()

        # test model blank and null fields validation
        with self.assertRaises(ValidationError) as err:
            person.full_clean()
        err_dict = err.exception.message_dict
        self.assertEquals(
            err_dict['name'][0],
            Person._meta.get_field('name').error_messages['blank'])
        self.assertEquals(
            err_dict['surname'][0],
            Person._meta.get_field('surname').error_messages['blank'])
        self.assertEquals(
            err_dict['email'][0],
            Person._meta.get_field('email').error_messages['blank'])
        self.assertEquals(
            err_dict['date_of_birth'][0],
            Person._meta.get_field('date_of_birth').
            error_messages['null'])

    def test_person_model_email_date_field_validation(self):
        """
        Test check validation email and date fields person model
        """
        person = Person()
        # test model email and date field validation
        person.email = 'aleks@'
        person.jabber = '42cc'
        person.date_of_birth = 'sd'
        with self.assertRaises(ValidationError) as err:
            person.full_clean()
        err_dict = err.exception.message_dict
        self.assertEquals(err_dict['email'][0],
                          EmailValidator.message)
        self.assertEquals(err_dict['jabber'][0],
                          EmailValidator.message)
        self.assertIn(Person._meta.get_field('date_of_birth').
                      error_messages['invalid'].format()[12:],
                      err_dict['date_of_birth'][0])

    def test_person_model_initial_data(self):
        """
        Test check that initial_data is in the database
        """
        # now check we can find initial_data in the database
        all_persons = Person.objects.all()
        self.assertEquals(len(all_persons), 1)
        only_person = all_persons[0]

        # and check that it's saved its attributes
        self.assertEquals(only_person.name, 'Aleks')
        self.assertEquals(only_person.surname, 'Woronow')
        self.assertEquals(only_person.email, 'aleks.woronow@yandex.ru')
        self.assertEquals(only_person.jabber, 'aleksw@42cc.co')
        self.assertEquals(only_person.skype_id, 'aleks_woronow')
        self.assertEquals(only_person.date_of_birth, date(2016, 2, 25))
        self.assertEquals(only_person.bio, 'I was born ...')
        self.assertEquals(str(only_person), 'Woronow Aleks')

    def test_person_model_image(self):
        """
        Test check that overwritten save method maintaining aspect ratio
        and reduce image to <= 200*200.
        """

        # save image file
        person = Person.objects.get(id=1)
        person.image = get_temporary_image()
        person.save()

        # check that height and width <= 200
        self.assertTrue(person.height <= 200)
        self.assertTrue(person.width <= 200)


class RequestStoreTest(TestCase):
    def test_request_store(self):
        """Test creating a new request and saving it to the database"""

        request_store = RequestStore()
        user = get_user_model().objects.get(id=1)

        # test model blank and null fields validation
        with self.assertRaises(ValidationError) as err:
            request_store.full_clean()
        err_dict = err.exception.message_dict
        self.assertEquals(err_dict['path'][0],
                          RequestStore._meta.get_field('path').
                          error_messages['blank'])
        self.assertEquals(err_dict['method'][0],
                          RequestStore._meta.get_field('method').
                          error_messages['blank'])

        # test cretae and save object
        request_store.path = '/'
        request_store.method = 'GET'
        request_store.user = user

        # check we can save it to the database
        request_store.save()

        # now check we can find it in the database again
        all_requests = RequestStore.objects.all()
        self.assertEquals(len(all_requests), 1)
        only_request = all_requests[0]
        self.assertEquals(str(only_request), str(request_store))

        # and check that it's saved its two attributes: path and method
        self.assertEquals(only_request.path, '/')
        self.assertEquals(only_request.method, 'GET')
        self.assertEquals(only_request.new_request, 1)
        self.assertEquals(only_request.priority, 0)
        self.assertEquals(only_request.user, user)

    def test_record_priority_field(self):
        """
        Test record priority field.
        """

        # pass to home page
        self.client.get(reverse('hello:home'))
        request_store = RequestStore.objects.first()

        # check record RequestStore contains:
        # method - 'GET' and default priority - 0
        self.assertEqual(request_store.path, '/')
        self.assertEqual(request_store.method, 'GET')
        self.assertEqual(request_store.priority, 0)

        # change priority to 1 and send POST to home page
        request_store.priority = 1
        request_store.save()
        self.client.post(reverse('hello:home'))

        # check record RequestStore contains:
        # method - 'POST' and priority - 1
        request_store = RequestStore.objects.first()
        self.assertEqual(request_store.method, 'POST')
        self.assertEqual

        
        self.client.get(reverse('hello:form'))

        # check record RequestStore contains:
        # method - 'GET' and priority - 0
        request_store = RequestStore.objects.last()
        self.assertEqual(request_store.method, 'GET')
        self.assertEqual(request_store.priority, 0)
        self.assertEqual(request_store.path, '/form/')


class NoteModelTestCase(TestCase):
    def setUp(self):
        self.data = dict(model='Person', inst='person', action_type=0)

    def test_notemodel(self):
        """
        Test creat, change and delete obbject notemodel.
        """
        # create note about person
        note_person = NoteModel.objects.create(**self.data)

        # take all objects of NoteModel: one - load init fixture, two - test
        all_note = NoteModel.objects.all()
        self.assertEqual(len(all_note), 2)
        only_note = all_note[1]
        self.assertEqual(only_note.model, note_person.model)
        self.assertEqual(only_note.action_type, 0)

        # change note about person to requeststore
        person_note = NoteModel.objects.get(id=note_person.id)
        person_note.model = 'RequestStore'
        person_note.inst = 'requeststore'
        person_note.action_type = 1
        person_note.save()

        # now note about requeststore action = 1
        person_note_change = NoteModel.objects.get(model='RequestStore')
        self.assertEqual(person_note_change.action_type, 1)

        # delete note person
        NoteModel.objects.all().delete()
        all_note = NoteModel.objects.all()
        self.assertEqual(all_note.count(), 0)

    def test_signal_processor(self):
        """
        Test signal processor records create,
        change and delete object.
        """
        # check action_type after created object (loaded fixtures) is 0
        note = NoteModel.objects.get(model='Person')
        self.assertEqual(note.action_type, 0)

        # check action_type after change object is 1
        person = Person.objects.first()
        person.name = 'Change'
        person.save()
        note = NoteModel.objects.filter(model='Person').last()
        self.assertEqual(note.action_type, 1)

        # check record after delete object is 2
        person = Person.objects.first()
        person.delete()
        note = NoteModel.objects.last()
        self.assertEqual(note.action_type, 2)
