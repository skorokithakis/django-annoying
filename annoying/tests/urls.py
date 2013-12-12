"""URLs for django-annoying's tests"""
from __future__ import absolute_import

from django.conf.urls import patterns
from . import views

urlpatterns = patterns('',
    (r'^ajax-request/$', views.ajax_request_view),
    (r'^ajax-request-httpresponse/$', views.ajax_request_httpresponse_view),
    (r'^render-to-content-type-kwarg/$', views.render_to_content_type_kwarg),
    (r'^render-to-mimetype-kwarg/$', views.render_to_mimetype_kwarg),
    (r'^render-to-content-type-positional/$', views.render_to_content_type_positional),
)
