# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm

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
        return self._html_output(
            normal_row='''<div class="form-group">
                           <div class="col-sm-2 control-label">%(label)s</div>
                           <div class="col-sm-4">%(field)s%(help_text)s</div>
                         </div>''',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <p class="help-block">%s</p>',
            errors_on_separate_row=True)
