# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django import template
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin

register = template.Library()

logger = logging.getLogger(__name__)


@register.inclusion_tag('templatetags/edit_link.html')
def edit_link(obj):
    if isinstance(obj, models.Model):
        model = ContentType.objects.get_for_model(obj)

        if model.model_class() in admin.site._registry:
            edit_link = '/admin/%s/%s/%d/' %\
                    (model.app_label, model.model, int(obj.id))
            return {
                'edit_link': edit_link,
            }
        else:
            logger.debug(
                'Set edit link for not register in admin "%s" model' % model)
    else:
        raise TypeError(
            'Invalide type arg for edit_link, shoud be models.Model instance')

    return None
