# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage


class HelloStorage(FileSystemStorage):
    def get_available_name(self, name):
        if self.exists(name):
            self.delete(name)
        return name
