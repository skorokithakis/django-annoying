"""URLs for django-annoying's tests"""
from __future__ import absolute_import

from django.conf.urls import patterns
from . import views

urlpatterns = patterns('',
    (r'^ajax-request/$', views.ajax_request_view),
    (r'^ajax-request-httpresponse/$', views.ajax_request_httpresponse_view),
)
