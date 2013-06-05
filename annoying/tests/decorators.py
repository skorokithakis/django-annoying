"""Tests for django-annoying's decorators"""

from django.test import TestCase

try:
    import json
except ImportError:
    from django.utils import simplejson as json

class AJAXRequestTestCase(TestCase):
    """Test cases for ajax_request"""
    urls = 'annoying.tests.urls'

    def setUp(self):
        self.RESPONSE_JSON = json.loads('{"int": 1, "list": [2, 3, 4], "bool": true, "date": "2013-12-25T15:16:00", "string": "barry", "dict": {"foo": "bar", "bar": "bob"}}')

    def test_defaults(self):
        response = self.client.get('/ajax-request/')
        self.assertEquals(json.loads(response.content), self.RESPONSE_JSON)
        self.assertTrue('application/json' in response['content-type'])

    def test_valid_header(self):
        response = self.client.get('/ajax-request/', HTTP_ACCEPT='text/json')
        self.assertEquals(json.loads(response.content), self.RESPONSE_JSON)
        self.assertTrue('text/json' in response['content-type'])

    def test_invalid_header(self):
        response = self.client.get('/ajax-request/', HTTP_ACCEPT='foo/bar')
        self.assertEquals(json.loads(response.content), self.RESPONSE_JSON)
        self.assertTrue('application/json' in response['content-type'])

    def test_httpresponse_check(self):
        response = self.client.get('/ajax-request-httpresponse/')
        self.assertEquals(response.content, "Data")
        self.assertTrue('text/html' in response['content-type'])
