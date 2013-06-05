"""Views for django-annoying's tests"""
from __future__ import absolute_import

from django.http import HttpResponse

from ..decorators import ajax_request

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
