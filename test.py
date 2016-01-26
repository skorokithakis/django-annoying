#!/usr/bin/env python
import sys
from os import path as osp

this = osp.splitext(osp.basename(__file__))[0]
BASE_DIR = osp.dirname(__file__)

from django.conf import settings

SETTINGS = dict(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': 'test.db'}},
    DEBUG=True,
    TEMPLATE_DEBUG=True,
    ROOT_URLCONF=this,
    INSTALLED_APPS=(
        'django.contrib.auth', 'django.contrib.contenttypes',
        'django.contrib.sessions', 'annoying', 'annoying.tests'
    ),
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                osp.join(BASE_DIR, 'annoying', 'tests', 'templates')
            ]
        }
    ]
)

# Check Django version and adjust settings for 1.6.
import django
from distutils.version import LooseVersion
django_version = django.get_version()
if LooseVersion(django_version) < LooseVersion('1.6'):
    raise ValueError("Django-annoying requires Django 1.6 or later.")
if LooseVersion(django_version) < LooseVersion('1.7'):
    del SETTINGS['TEMPLATES']
    SETTINGS['TEMPLATE_DIRS'] = [
        osp.join(BASE_DIR, 'annoying', 'tests', 'templates')
    ]

if not settings.configured:
    settings.configure(**SETTINGS)

try:
    from django.conf.urls import patterns
except ImportError:
    # Hack for backwards-compatibility.
    patterns = lambda *x: list(x[1:])

urlpatterns = patterns('', )

if __name__ == '__main__':
    try:
        # Override Apps module to work with us
        from django.apps.registry import Apps
        get_containing_app_config_orig = Apps.get_containing_app_config

        def get_containing_app_config(Apps_object, *args, **kwargs):
            Apps_object.apps_ready = True
            return get_containing_app_config_orig(Apps_object, *args, **kwargs)

        Apps.get_containing_app_config = get_containing_app_config

    except ImportError:
        # override get_app to work with us for Django 1.6.
        from django.db import models
        get_app_orig = models.get_app

        def get_app(app_label, *a, **kw):
            if app_label == this:
                return sys.modules[__name__]
            return get_app_orig(app_label, *a, **kw)

        models.get_app = get_app

    from django.core import management
    management.execute_from_command_line(["test.py", "test", "annoying.tests"])
