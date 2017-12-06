# container for context
secrets = {"user_name": "", "password": ""}

import requests # used to issue CRUD requests, the meat and 'taters of this thing
import base64 as base64 # used with the login with certificate functions
from random import choice # used with the login with certificate functions
from string import ascii_uppercase #used with the login with certificate functions
import json # Interact API returns a lot of json-like text objects, we use this to bind them to python objects
from secret import secrets as secret # this should get removed, but can be used to store a local password! crazy... but Interact has additional security measures on top of your user login / password and these aren't stored anywhere else than your local machine or app server. if you can encrypt/decrypt them yourself... please do! TODO: proper password prompting/storage
from .containers import rules # our own rules for data objects. the API should return reponses for bad requests of course, but I'll do my best to define input rules and user feedback prior to issuing the request. 

print(secret) # TODO: delete this!
print(rules) # TODO: delete this!

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
            secret["user_name"], 
            secret["password"]
        ).text
    )

# General purpose build for get requests to Interact API
def get(service_url, **kwargs):
    context = get_context()
    auth_token = context["authToken"]
    endpoint = f'{context["endPoint"]}/{api_url}/{service_url}'
    headers = kwargs.get('headers', {'Authorization' : auth_token})
    if "parameters" in kwargs: # use parameters if we got them
        parameters = kwargs.get('parameters', None)
        endpoint = f'{endpoint}?{parameters}'
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
def login(user_name=secret['user_name'], password=secret['password'], url=login_url):
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
# TODO: fix 403 response
def merge_or_update_members_in_a_profile_list_table(list_name, **kwargs):
    data = rules["merge_or_update_members_in_a_profile_list_table"][0] # load container data
    # process keyword arguments
    fields = kwargs.get('fields')
    records = kwargs.get('records', None)
    merge_rules = kwargs.get('merge_rules', data["mergeRule"])

    if isinstance(fields, list) and isinstance(records, list): # make sure the input fields and records are lists
        if len(fields) == len(records): # make sure the fields and records have the same amount of columns
            data["recordData"]["fieldNames"] = fields # insert our fields into the data 
            data["recordData"]["records"] = records # insert our records into the data
        else:
            raise ValueError("ERROR: List headers count does not match record column count")
    else:
        raise ValueError("ARGUMENT ERROR: input fields or records are not list objects.\nPlease specify lists for 'fields' or 'records' arguments.")

    rules_keys = [key for key in data["mergeRule"]] # extract merge rules 
    rules_values = [data["mergeRule"][rule]["default"] for rule in rules_keys] # extract merge rules default values
    rules_dict = dict(zip(rules_keys, rules_values)) # assign a new rules object to work on before we insert it into the request object

    for merge_rule, merge_value in merge_rules.items():
        try:
            if merge_value in data["mergeRule"][merge_rule]["options"]: # if the user input merge rule value is valid based on the container data
                data["mergeRule"][merge_rule] = merge_value # add the new merge rule value to the data
        except KeyError:
            print(f'ERROR: Merge rule "{merge_rule}" is not valid. Valid merge rules are:\n{rules_keys}')
        # print(merge_rule + " : " + merge_value)

        rules_dict[merge_rule] = merge_value # assign the parameters supplied in the merge_rules keyword argument to the new rules
    data["mergeRule"] = rules_dict # add the merge rules back into the data

    # build post request
    context = get_context()
    auth_token = context["authToken"]
    url = f'{context["endPoint"]}/{api_url}/lists/{list_name}/members'
    headers = {'Authorization' : auth_token, 'Content-Type' : 'application/json'}
    print(json.dumps(data))
    response = requests.post(url, data=json.dumps(data), headers=headers) # make the request
    data = rules["merge_or_update_members_in_a_profile_list_table"][0] # return the data to the container?
    return response
# Or use a more sensible name
def list_manage(list_name, **kwargs):
    return merge_or_update_members_in_a_profile_list_table(list_name, **kwargs)

# Retrieve a member of a profile list using RIID
def retrieve_a_member_of_a_profile_list_using_riid(list_name, riid):
    service_url = f'lists/{list_name}/members/{riid}'
    return get(service_url, parameters='fs=all') # only support returning all fields for now # TODO: implement other fields
# Or use a more sensible name
def get_member_of_list_by_riid(list_name, riid):
    return retrieve_a_member_of_a_profile_list_using_riid(list_name, riid)

# Retrieve a member of a profile list based on query attribute
def retrieve_a_member_of_a_profile_list_based_on_query_attribute(list_name, record_id, query_attribute='c', fields_to_return='all'):
    query_attributes_allowed = [
        'r', # RIID
        'e', # EMAIL_ADDRESS
        'c', # CUSTOMER_ID
        'm'  # MOBILE_NUMBER
    ]
    try:
        query_attribute in query_attributes_allowed
    except:
        raise ValueError(f"Query attribute is not one of {query_attributes_allowed}")
    service_url = f'lists/{list_name}/members/'
    return get(service_url, parameters=f'fs={fields_to_return}&qa={query_attribute}&id={record_id}')
# Or use a more sensible name
def get_member_of_list_by_id(list_name, record_id, query_attribute='c', fields_to_return='all'):
    return retrieve_a_member_of_a_profile_list_based_on_query_attribute(list_name, record_id, query_attribute='c', fields_to_return='all')

# Delete Profile List Recipients based on RIID
# TODO: fix 403 response
def delete_profile_list_recipients_based_on_riid(list_name, riid):
    context = get_context()
    auth_token = context["authToken"]
    endpoint = f'{context["endPoint"]}/lists/{list_name}/members/{riid}'
    headers = {'Authorization' : auth_token}
    response = requests.delete(url=endpoint, headers=headers)
    return response
# Or use a more sensible name
def delete_from_profile_list(list_name, riid):
    return delete_profile_list_recipients_based_on_riid(list_name, riid)

# Retrieve all profile extentions of a profile list
def retrieve_all_profile_extensions_of_a_profile_list(list_name):
    return get(f'lists/{list_name}/listExtensions')
# Or use a more sensible name
def get_profile_extensions(list_name):
    return retrieve_all_profile_extensions_of_a_profile_list(list_name)

# Create a new profile extension table
# TODO: fix 403 response
def create_a_new_profile_extension_table(list_name, folder_name='___api-generated', extension_name='_pet', default_field_type='STR4000'):
    extension_name = f'{list_name}{extension_name}'
    data = {
        "profileExtension" : {
            "objectName" : extension_name,
            "folderName" : folder_name,
            "fields" :
            [
                {
                    "fieldName" : "edu",
                    "fieldType" : default_field_type # Could be STR500, STR4000, INTEGER, NUMBER, or TIMESTAMP
                }
            ]
        }
    }
    context = get_context()
    auth_token = context["authToken"]
    endpoint = f'{context["endPoint"]}/lists/{list_name}/listExtensions'
    headers = {'Authorization' : auth_token, 'Content-Type' : 'application/json'}
    response = requests.post(url=endpoint, headers=headers)
    return response
# Or use a more sensible name
def create_profile_extension(list_name, folder_name='___api-generated', extension_name='_pet', default_field_type='STR4000'):
    return create_a_new_profile_extension_table(list_name, folder_name='___api-generated', extension_name='_pet', default_field_type='STR4000')

# TODO: Merge or update members in a profile extension table 
def merge_or_update_members_in_a_profile_extension_table():
    return
# Or use a more sensible name
def profile_list_manage():
    return merge_or_update_members_in_a_profile_extension_table()

# TODO: Retrieve a member of a profile extension table based on RIID
def retrieve_a_member_of_a_profile_extension_table_based_on_riid(list_name, profile_extension_name, riid, fields_to_return='all'):
    return 
# Or use a more sensible name
def get_member_of_profile_extension_by_riid(list_name, profile_extension_name, riid, fields_to_return='all'):
    return retrieve_a_member_of_a_profile_extension_table_based_on_riid(list_name, profile_extension_name, riid, fields_to_return='all')

##################
# Extra features #
##################

# Find what lists a record is in by the input RIID, Email Address or Mobile Number
def get_lists_for_record(riid):
    all_lists = [list_name["name"] for list_name in profile_lists()] # get a list of all the profile list names
    member_of = [] # container list
    for profile_list in all_lists:
        response = retrieve_a_member_of_a_profile_list_using_riid(profile_list, riid)
        if "recordData" in response: # if the member (by riid) is in the profile list, add it to the list of profiles all_lists
            member_of.append(profile_list) 
    return member_of

