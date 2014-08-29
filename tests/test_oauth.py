import sys
import unittest

sys.path.insert(0, '../')

from lib import oauth2

class Response:
    def __init__(self, text):
        self.text = text


class Test_Oauth(unittest.TestCase):
    def setUp(self):
        self.consumer = oauth2.Consumer('test_client_id', 'test_client_secret')

    def test_authorize(self):
        auth_url = 'https://localhost/'
        expected = 'Go to ' + auth_url + '?client_id=test_client_id&response_type=test in a web browser!'
        actual = self.consumer.authorize(auth_url, 'test')
        self.assertEquals(expected, actual)

    def test_authorize_with_kwargs(self):
        auth_url = 'https://localhost/'
        expected = 'Go to ' + auth_url + '?client_id=test_client_id&response_type=test&test_kwarg=test_value in a web browser!'
        actual = self.consumer.authorize(auth_url, 'test', test_kwarg='test_value')
        self.assertEquals(expected, actual)

    def test_get_request_token(self):
        oauth2.requests.post = lambda url, data=None, **kwargs : Response(
            '{"refresh_token": "test_refresh_token"}'
        )
        expected = 'test_refresh_token'
        actual = self.consumer.get_request_token(
            'https://localhost/', 
            'pin'
        )
        self.assertEquals(expected, actual)

    def test_get_access_token(self):
        oauth2.requests.post = lambda url, data=None, **kwargs : Response(
            '{"access_token": "test_access_token"}'
        )
        expected = 'test_access_token'
        actual = self.consumer.get_access_token(
            'https://localhost/',
            'test_refresh_token'
        )
        self.assertEquals(expected, actual)

    def test_api_request_get(self):
        oauth2.requests.get = lambda url, **kwargs : Response(
            '{"test_get_response": "test_content"}'
        )
        expected = {'test_get_response': 'test_content'}
        actual = self.consumer.api_request_get(
            'http://localhost/',
            'test_access_token'
        )
        self.assertEquals(expected, actual)

    def test_api_request_post(self):
        oauth2.requests.post = lambda url, data=None, **kwargs : Response(
            '{"test_post_response": "test_content"}'
        )
        expected = {'test_post_response': 'test_content'}
        actual = self.consumer.api_request_post(
            'http://localhost/',
            'test_access_token'
        )
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()
