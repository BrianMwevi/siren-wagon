import json
import requests
from decouple import config
from requests.auth import HTTPBasicAuth


def request_new_token():
    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')
    auth_url = config('AUTHENTICATION_URL')

    response = requests.request('GET', auth_url,
                                auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return json.loads(response.text.encode('utf8')).values()
