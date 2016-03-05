# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.template import Context, loader

from .models import Person


class CalendarWidget(forms.DateInput):
    class Media:
        js = ('https://code.jquery.com/ui/1.11.0/jquery-ui.js',)

    def __init__(self, attrs={}):
        super(CalendarWidget, self).__init__(
            attrs={'class': 'form-control datepicker', 'size': '10'})


class PersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'image' and field_name != 'date_of_birth':
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Person
        fields = ['name', 'surname', 'date_of_birth', 'bio',
                  'email', 'jabber', 'skype_id', 'other', 'image']
        widgets = {
            'date_of_birth': CalendarWidget(),
            'image': forms.FileInput()
        }

    class Media:
        js = ('js/change_person_data.js',)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def as_div(self):
        normal_attr = Context({
            'class_label': 'col-sm-2 control-label',
            'class_input': 'col-sm-4',
            'class_help_text': 'help-block'})

        normal_tmpl = loader.get_template('form/normal_row.html')
        ender_tmpl = loader.get_template('form/row_ender.html')
        help_text_tmpl = loader.get_template('form/help_text.html')

        return self._html_output(
            normal_row=normal_tmpl.render(normal_attr),
            error_row='%s',
            row_ender=ender_tmpl.render(Context()),
            help_text_html=help_text_tmpl.render(normal_attr),
            errors_on_separate_row=True)
