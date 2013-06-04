"""Tests for django-annoying's decorators"""

from django.test import TestCase

class AJAXRequestTestCase(TestCase):
    """Test cases for ajax_request"""
    urls = 'annoying.tests.urls'

    def setUp(self):
        self.RESPONSE_JSON = '{"int": 1, "list": [2, 3, 4], "bool": true, "string": "barry", "dict": {"foo": "bar", "bar": "bob"}}'

    def compare_response(self, response, expected_data, content_type='application/json', status_code=200):
        """Compare expected results with actual response"""
        self.assertEquals(response.content, expected_data)
        self.assertEquals(response.status_code, status_code)
        self.assertTrue(content_type in response['content-type'])

    def test_defaults(self):
        response = self.client.get('/ajax-request/')
        self.compare_response(response, self.RESPONSE_JSON)

    def test_valid_header(self):
        response = self.client.get('/ajax-request/', HTTP_ACCEPT='text/json')
        self.compare_response(response, self.RESPONSE_JSON, content_type='text/json')

    def test_httpresponse_check(self):
        response = self.client.get('/ajax-request-httpresponse/')
        self.compare_response(response, "Data", content_type='text/html')
