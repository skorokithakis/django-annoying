"""URLs for django-annoying's tests"""
from __future__ import absolute_import

from django.conf.urls import url
from . import views

import django
from distutils.version import StrictVersion
django_version = django.get_version()

# Use old URL Conf settings for Django <= 1.8.
if StrictVersion(django_version) < StrictVersion('1.8.0'):
    from django.conf.urls import patterns
    urlpatterns = patterns('',
        (r'^ajax-request/$', views.ajax_request_view),
        (r'^ajax-request-httpresponse/$', views.ajax_request_httpresponse_view),
        (r'^render-to-content-type-kwarg/$', views.render_to_content_type_kwarg),
        (r'^render-to-mimetype-kwarg/$', views.render_to_mimetype_kwarg),
        (r'^render-to-content-type-positional/$', views.render_to_content_type_positional),
    )
else:
    urlpatterns = [
        url(r'^ajax-request/$', views.ajax_request_view),
        url(r'^ajax-request-httpresponse/$', views.ajax_request_httpresponse_view),
        url(r'^render-to-content-type-kwarg/$', views.render_to_content_type_kwarg),
        url(r'^render-to-mimetype-kwarg/$', views.render_to_mimetype_kwarg),
        url(r'^render-to-content-type-positional/$', views.render_to_content_type_positional),
    ]
