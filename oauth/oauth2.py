import json
import requests
import webbrowser

AUTH_URL = 'https://api.imgur.com/oauth2/authorize'
TOKEN_URL = 'https://api.imgur.com/oauth2/token'
RESPONSE_TYPE = 'pin'

def authorize(client_id, client_secret):
    url = '{0}?client_id={1}&response_type={2}'.format(
        AUTH_URL, client_id, RESPONSE_TYPE
    )

    print 'Go to {0} in a webrowser!'.format(url)
    pin = raw_input('Please enter the PIN provided by the website: ')

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'pin',
        'pin': pin
    }
    r = requests.post(TOKEN_URL, data=json.dumps(payload))
    refresh_token = json.loads(r.text)['refresh_token']
