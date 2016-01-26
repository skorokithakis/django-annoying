"""Views for django-annoying's tests"""
from __future__ import absolute_import

from django.http import HttpResponse

from ..decorators import ajax_request, render_to

import datetime


@ajax_request
def ajax_request_view(request):
    return {
        'bool': True,
        'int': 1,
        'list': [2, 3, 4],
        'dict': {
            'foo': 'bar',
            'bar': 'bob',
        },
        'string': 'barry',
        'date': datetime.datetime(2013, 12, 25, 15, 16),
    }


@ajax_request
def ajax_request_httpresponse_view(request):
    return HttpResponse("Data")


@render_to('test.txt', content_type='text/plain')
def render_to_content_type_kwarg(request):
    return {}


@render_to('test.txt', mimetype='text/plain')
def render_to_mimetype_kwarg(request):
    return {}


@render_to('test.txt', 'text/plain')
def render_to_content_type_positional(request):
    return {}
