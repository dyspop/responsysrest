# container for context
secrets = {"user_name": "", "password": ""}

import requests
import base64 as base64
import json
from secret import secrets
from random import choice
from string import ascii_uppercase

print(secrets)

headers = {'content-type' : 'application/x-www-form-urlencoded'}
base_url = 'http://login5.responsys.net/rest/api/v1.3/'

# Helper functions for use with direct implementations of calls as below

# # Helps with Login with username and certificates
# def generate_client_challenge_value(length=16):
#     return base64.b64encode(bytes(''.join(choice(ascii_uppercase) for i in range(16)), 'utf-8'))

# Direct implentations of calls from Responsys Interact REST API documentation
# https://docs.oracle.com/cloud/latest/marketingcs_gs/OMCEB/OMCEB.pdf
# All function names and comment descriptions are directly from the v1.3 REST API documentation, except some English-language inconsistencies are modified from their documentation and code-comment style to match PEP-8 for their corresponding function/method names.

# Login with username and password
def login_with_username_and_password(url, user_name, password):
    service_url = 'auth/token'
    url = url + service_url
    data = {
        "user_name" : user_name,
        "password" : password,
        "auth_type" : "password"
    }
    return requests.post(url, data=data, headers=headers)

# # TODO: Implement 
# # Login with username and certificates
# def login_with_username_and_certificates(url, user_name):
#     # Step 1 - Authenticate server by sending the following REST request
#     data = {
#         "user_name" : user_name,
#         "auth_type" : "server",
#         "client_challenge" : client_challenge_value
#     }
#     service_url = 'auth/token'
#     url = url + service_url
#     client_challenge_value = generate_client_challenge_value()

#     # Step 2 - Get response from the server and decrypt with RSA and Public Key Certificate (downloaded from Interact interface)
#     response = requests.post(url, data=data, headers=headers)
#     # TODO: Implement parse response
#     # Expect:
#     # {
#     #     "authToken" : "<TEMP_AUTH_TOKEN>",
#     #     "serverChallenge" : "<BASE_64_ENCODED_SERVER_CHALLENGE>",
#     #     "clientChallenge" : "<ENCRYPTED_AND_THEN_BASE_64_ENCODED_CLIENT_CHALLENGE>"
#     # }
#     response = parse_response()
#     # TODO: Implement import certificate
#     certificate = import_local_public_key_certificate(file)
#     # TODO: Implement RSA decryption
#     response = decrypt(response)
#     # TODO: Implement authorize call
#     response = login_with_username_and_certificate_authorization(
#         user_name, 
#         auth_type=client, 
#         server_challenge=encrypt(response["serverChallenge"])
#     )

#     return response

# # TODO: Implement
# # Refresh token
# def refresh_token(url, old_auth_token):
#     service_url = 'auth/token'
#     url = url + service_url
#     data = {'auth_type' : 'token'}
#     headers = {'Authorization' : auth_token}
#     response = requests.post(url, data=data, headers=headers)
#     return response

# Retrieving all profile lists for an account
def retrieve_all_profile_lists(url):
    service_url = 'lists'
    url = url + service_url
    auth_token = json.loads(
        login_with_username_and_password(
            base_url, 
            secrets["user_name"], 
            secrets["password"]
        ).text
    )["authToken"]
    headers = {'Authorization' : auth_token}
    response = requests.get(url, headers=headers)
    return response

