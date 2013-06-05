"""Settings for the test project"""
import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db',
    }
}

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'

SETTINGS_ROOT = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(SETTINGS_ROOT, '../..'))

MEDIA_ROOT = os.path.join(SETTINGS_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(SETTINGS_ROOT, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '5$y^4xltxzcqtgohfzu!d&769461tadpx+2hvv#zgcy2i$t*n3'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'test_project.urls'

WSGI_APPLICATION = 'test_project.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_extensions',
    'annoying',
)
