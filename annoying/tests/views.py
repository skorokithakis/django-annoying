"""Views for django-annoying's tests"""
from __future__ import absolute_import

from django.http import HttpResponse

from ..decorators import ajax_request

RESPONSE_DICT = {
    'bool': True,
    'int': 1,
    'list': [2, 3, 4],
    'dict': {
        'foo': 'bar',
        'bar': 'bob',
    },
    'string': 'barry',
}

@ajax_request
def ajax_request_view(request):
    return RESPONSE_DICT

@ajax_request
def ajax_request_httpresponse_view(request):
    return HttpResponse("Data")
