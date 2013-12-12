#!/usr/bin/env python
import sys
from os import path as osp

this = osp.splitext(osp.basename(__file__))[0]
BASE_DIR = osp.dirname(__file__)

from django.conf import settings
SETTINGS = dict(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'test.db'}},
    DEBUG=True,
    TEMPLATE_DEBUG=True,
    ROOT_URLCONF=this,
    INSTALLED_APPS=('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'annoying'),
    TEMPLATE_DIRS=(osp.join(BASE_DIR, 'annoying', 'tests', 'templates'),),
)

if not settings.configured:
    settings.configure(**SETTINGS)

from django.db import models
from django.conf.urls import patterns

urlpatterns = patterns('',)

if __name__ == '__main__':
    # override get_app to work with us
    get_app_orig = models.get_app
    def get_app(app_label, *a, **kw):
        if app_label == this:
            return sys.modules[__name__]
        return get_app_orig(app_label, *a, **kw)
    models.get_app = get_app

    models.loading.cache.app_store[type(this + '.models', (), {'__file__':__file__})] = this

    from django.core import management
    management.execute_from_command_line(["test.py", "test", "annoying"])
