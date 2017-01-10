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

# Check Django version and adjust settings.
import django
from distutils.version import LooseVersion
django_version = django.get_version()
if LooseVersion(django_version) < LooseVersion('1.8'):
    raise ValueError("Django-annoying requires Django 1.8 or later.")

if not settings.configured:
    settings.configure(**SETTINGS)

urlpatterns = []

if __name__ == '__main__':
    # Override Apps module to work with us
    from django.apps.registry import Apps
    get_containing_app_config_orig = Apps.get_containing_app_config

    def get_containing_app_config(Apps_object, *args, **kwargs):
        Apps_object.apps_ready = True
        return get_containing_app_config_orig(Apps_object, *args, **kwargs)

    Apps.get_containing_app_config = get_containing_app_config

    from django.core import management
    management.execute_from_command_line(["test.py", "test", "annoying.tests"])
