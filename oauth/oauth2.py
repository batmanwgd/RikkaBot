import json
import requests

class Consumer:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def authorize(self, auth_url, token_url, **kwargs):
        url = '{0}?client_id={1}'.format(auth_url, self.client_id)
        if kwargs:
            url += '&{0}'.format('&'.join(
                ['{0}={1}'.format(key, val) for key, val in kwargs.items()]
            ))

        print 'Go to {0} in a webrowser!'.format(url)
        pin = raw_input('Please enter the PIN provided by the website: ')

        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'pin',
            'pin': pin
        }
        r = requests.post(token_url, data=json.dumps(payload))
        return json.loads(r.text)['refresh_token']

    def get_access_token(self, token_url, refresh_token):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        r = requests.post(token_url, data=json.dumps(payload))
        return json.loads(r.text)['access_token']

    def api_request(self, url, headers):
        r = requests.get(url, headers=headers)
        return json.loads(r.text)['data']
