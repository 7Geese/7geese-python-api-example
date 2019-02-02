import sys
from urlparse import urljoin

import requests

BASE_URL = 'https://app.7geese.com/'
TOKEN_URL = urljoin(BASE_URL, '/o/token/')
API_URL = urljoin(BASE_URL, '/api/v/2.0/')

credentials = {
    'username': '',
    'password': '',
    'client_id': '',
    'client_secret': '',
}


def handle_response_errors(response):
    if response.status_code != 200:
        print('HTTP Status Code {}'.format(response.status_code))
        print(response.json())
        sys.exit(1)


def get_access_token():
    auth = (credentials['client_id'], credentials['client_secret'])
    r = requests.post(TOKEN_URL, data={
        'grant_type': 'password',
        'username': credentials['username'],
        'password': credentials['password'],
        'scope': ['all'],
    }, auth=auth)
    handle_response_errors(r)
    return r.json()['access_token']


def get_authenticated(access_token, path):
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    url = urljoin(API_URL, path)
    r = requests.get(url, headers=headers)
    handle_response_errors(r)
    return r.json()


access_token = get_access_token()

print('In your network, there are:')

resp = get_authenticated(access_token, 'objectives')
print('- {} objectives'.format(resp['count']))

resp = get_authenticated(access_token, 'recognitions')
print('- {} recognitions'.format(resp['count']))
