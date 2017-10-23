"""URLs for django-annoying's tests"""
from __future__ import absolute_import

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ajax-request/$', views.ajax_request_view),
    url(r'^ajax-request-httpresponse/$', views.ajax_request_httpresponse_view),
    url(r'^render-to-content-type-kwarg/$', views.render_to_content_type_kwarg),
    url(r'^render-to-content-type-positional/$', views.render_to_content_type_positional),
]
