# container for context
secrets = {"user_name": "", "password": ""}

import requests
import base64 as base64
import json
from secret import secrets
from random import choice
from string import ascii_uppercase
from .containers import rules

print(secrets)
print(rules)

api_url = 'rest/api/v1.3'
login_url = f'http://login5.responsys.net/{api_url}/'

# Helper functions for use with direct implementations of calls as below

# # Helps with Login with username and certificates
# def generate_client_challenge_value(length=16):
#     return base64.b64encode(bytes(''.join(choice(ascii_uppercase) for i in range(16)), 'utf-8'))

# Return the login response as context, used with each individual call
# TODO: figure out how to log out after each log in!
def get_context():
    return json.loads(
        login_with_username_and_password(
            secrets["user_name"], 
            secrets["password"]
        ).text
    )

# General purpose build for get requests to Interact API
def get(service_url, **kwargs):
    context = get_context()
    auth_token = context["authToken"]
    endpoint = f'{context["endPoint"]}/{api_url}/{service_url}'
    headers = kwargs.get('headers', {'Authorization' : auth_token})
    response = json.loads(requests.get(url=endpoint, headers=headers).text)
    return response

# Direct implentations of calls from Responsys Interact REST API documentation
# https://docs.oracle.com/cloud/latest/marketingcs_gs/OMCEB/OMCEB.pdf
# All function names and comment descriptions are directly from the v1.3 REST API documentation, except some English-language inconsistencies are modified from their documentation and code-comment style to match PEP-8 for their corresponding function/method names.
# Many functions are mapped to another name afterwards as well for ease of use.

# Login with username and password
def login_with_username_and_password(user_name, password, url=login_url):
    url = f'{login_url}auth/token'
    data = {
        "user_name" : user_name,
        "password" : password,
        "auth_type" : "password"
    }
    headers = {'content-type' : 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=data, headers=headers)
    return response
# Or use a more sensible name
def login(user_name, password, url=login_url):
    return login_with_username_and_password(user_name, password, url=login_url)

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
def retrieving_all_profile_lists_for_an_account():
    return get('lists')
# Or use a more sensible name
def profile_lists():
    return retrieving_all_profile_lists_for_an_account()

# Get all EMD email campaigns
def get_all_emd_email_campaigns():
    return get('campaigns')
# Or use a more sensible name
def campaigns():
    return get_all_emd_email_campaigns()

# Merge or update members in a profile list table
def merge_or_update_members_in_a_profile_list_table(listName):
    context = get_context()
    auth_token = context["authToken"]
    endpoint = f'{context["endPoint"]}/{api_url}/lists/{listName}/members'
    headers = {'Authorization' : auth_token, 'Content-Type' : 'application/json'}
    data = rules["merge_or_update_members_in_a_profile_list_table"]
    # response = requests.post(url)
    return data
# Or use a more sensible name
def list_manage(listName):
    return merge_or_update_members_in_a_profile_list_table(listName)
