# container for context
secrets = {"user_name": "", "password": ""}

import requests
from secret import secrets
from random import choice
from string import ascii_uppercase

print(secrets)

headers = {'content-type': 'application/x-www-form-urlencoded'}
base_url = 'http://login5.responsys.net/rest/api/v1.3/'

# Helper functions for use with direct implementations of calls as below
def generate_client_challenge_value(length=16):
    return base64.b64encode(''.join(choice(ascii_uppercase) for i in range(length)))

# Direct implentations of calls from Responsys Interact REST API documentation
def login_with_username_and_password(url, user_name, password):
    service_url = 'auth/token'
    url = url + service_url
    data = {
        "user_name" : user_name,
        "password" : password,
        "auth_type" : "password"
    }
    return requests.post(url, data=data, headers=headers)

def login_with_username_and_certificates(url, user_name):
    service_url = 'auth/token'
    url = url + service_url
    client_challenge_value = generate_client_challenge_value()
    data = {
        "user_name" : user_name,
        "auth_type" : "server",
        "client_challenge" : client_challenge_value
    }
    response = requests.post(url, data=data, headers=headers)
