"""Python client library for the Responsys Interact REST API"""

__version__ = "0.1.0"
__keywords__ = "responsys interact client rest api"

# container for context
secrets = {"user_name": "", "password": ""}

import requests
from secret import secrets

print(secrets)

headers = {'content-type': 'application/x-www-form-urlencoded'}
base_url = 'http://login5.responsys.net/rest/api/v1.3/'

def login_with_username_and_password(url, user_name, password):
    service_url = 'auth/token'
    data = {
        "user_name" : user_name,
        "password" : password,
        "auth_type" : "password"
    }
    url = url + service_url
    return requests.post(url, data=data, headers=headers)