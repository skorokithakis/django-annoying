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
        self.assertEqual(json.loads(response.content.decode('utf8')), self.RESPONSE_JSON)
        self.assertTrue('application/json' in response['content-type'])

    def test_valid_header(self):
        response = self.client.get('/ajax-request/', HTTP_ACCEPT='text/json')
        self.assertEqual(json.loads(response.content.decode('utf8')), self.RESPONSE_JSON)
        self.assertTrue('text/json' in response['content-type'])

    def test_invalid_header(self):
        response = self.client.get('/ajax-request/', HTTP_ACCEPT='foo/bar')
        self.assertEqual(json.loads(response.content.decode('utf8')), self.RESPONSE_JSON)
        self.assertTrue('application/json' in response['content-type'])

    def test_httpresponse_check(self):
        response = self.client.get('/ajax-request-httpresponse/')
        self.assertEqual(response.content, b"Data")
        self.assertTrue('text/html' in response['content-type'])


class RenderToTestCase(TestCase):
    """Test cases for render_to"""
    urls = 'annoying.tests.urls'

    def test_content_type_kwarg(self):
        response = self.client.get('/render-to-content-type-kwarg/')
        self.assertTrue('text/plain' in response['content-type'])

    def test_mimetype_kwarg(self):
        response = self.client.get('/render-to-mimetype-kwarg/')
        self.assertTrue('text/plain' in response['content-type'])

    def test_content_type_positional(self):
        response = self.client.get('/render-to-content-type-positional/')
        self.assertTrue('text/plain' in response['content-type'])
