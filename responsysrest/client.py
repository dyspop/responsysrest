"""Responsys REST API Client."""
# used to issue CRUD requests, the meat and 'taters of this thing
import requests

# used with the login with certificate functions
# import base64 as base64

# Interact API returns a lot of json-like text objects
# we use this to bind them to python objects
import json

# used with the login with certificate functions
# from random import choice

# used with the login with certificate functions
# from string import ascii_uppercase

# this should get removed, but can be used to store a local password!
# crazy... but Interact has additional security measures
# on top of your user login / password and these aren't stored
# anywhere else than your local machine or app server.
# If you can encrypt/decrypt them yourself... please do!
# TODO: proper password prompting/storage
from secret import secrets as secret
# our own rules for data objects.
from .containers import rules

# TODO: delete this!
print(secret)

api_url = 'rest/api/v1.3'
login_url = f'http://login5.responsys.net/{api_url}/'

# Helper functions for use with direct implementations of calls as below

# # Helps with Login with username and certificates
# def generate_client_challenge_value(length=16):
#     return base64.b64encode(
#         bytes(''.join(choice(ascii_uppercase) for i in range(16)), 'utf-8')
#     )


def get_context():
    """
    Return the login response as context.

    Used with each individual call to Responsys API.
    """
    # TODO: figure out how to log out after each log in!
    context = json.loads(
        login(
            secret["user_name"],
            secret["password"]
        ).text
    )
    return context


def get(service_url, **kwargs):
    """General purpose build for GET requests to Interact API."""
    context = get_context()
    auth_token = context["authToken"]
    endpoint = f'{context["endPoint"]}/{api_url}/{service_url}'
    headers = kwargs.get('headers', {'Authorization': auth_token})
    # use parameters if we got them
    if "parameters" in kwargs:
        parameters = kwargs.get('parameters', None)
        endpoint = f'{endpoint}?{parameters}'
    return json.loads(requests.get(url=endpoint, headers=headers).text)


# Direct implentations of calls from Responsys Interact REST API documentation
# https://docs.oracle.com/cloud/latest/marketingcs_gs/OMCEB/OMCEB.pdf
# All function names and comment descriptions are directly from the
# v1.3 REST API documentation, except some English-language inconsistencies
# are modified from their documentation and code-comment style to match PEP-8
# for their corresponding function/method names.
# Many functions are mapped to another name afterwards as well for ease of use.


def login(user_name, password, url=login_url):
    """Login with username and password."""
    url = f'{login_url}auth/token'
    data = {
        "user_name": user_name,
        "password": password,
        "auth_type": "password"
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
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

#     # Step 2 - Get response from the server and decrypt with RSA and
#     # Public Key Certificate (downloaded from Interact interface)
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


def get_profile_lists():
    """Retrieving all profile lists for an account."""
    return get('lists')


def get_campaigns():
    """Get all EMD email campaigns."""
    return get('campaigns')


# Merge or update members in a profile list table
# TODO: fix 403 response
def manage_profile_list(list_name, **kwargs):
    """Merge or update members in a profile list table."""
    # load container data
    data = rules["merge_or_update_members_in_a_profile_list_table"][0]
    # process keyword arguments
    fields = kwargs.get('fields')
    records = kwargs.get('records', None)
    merge_rules = kwargs.get('merge_rules', data["mergeRule"])

    # make sure the input fields and records are lists
    if isinstance(fields, list) and isinstance(records, list):
        # make sure the fields and records have the same amount of columns
        if len(fields) == len(records):
            # insert our fields into the data
            data["recordData"]["fieldNames"] = fields
            # insert our records into the data
            data["recordData"]["records"] = records
        else:
            raise ValueError(
                """ERROR: List headers count does not
                match record column count"""
            )
    else:
        raise ValueError(
            """
            ARGUMENT ERROR: input fields or records are not list objects.\n
            Please specify lists for 'fields' or 'records' arguments.
            """
        )
    # extract merge rules
    rules_keys = [key for key in data["mergeRule"]]
    # extract merge rules default values
    rules_values = [
        data["mergeRule"][rule]["default"] for rule in rules_keys
    ]
    # assign a new rules object to work on before we insert it into the
    # request object
    rules_dict = dict(zip(rules_keys, rules_values))

    for merge_rule, merge_value in merge_rules.items():
        try:
            # if the user input merge rule value is valid based on the
            # container data
            if merge_value in data["mergeRule"][merge_rule]["options"]:
                # add the new merge rule value to the data
                data["mergeRule"][merge_rule] = merge_value
        except KeyError:
            print(
                """
                f'ERROR: Merge rule "{merge_rule}" is not valid.
                Valid merge rules are:
                {rules_keys}'
                """
            )
        # print(merge_rule + " : " + merge_value)
        # assign parameters from merge_rules keyword arguments to new rules
        rules_dict[merge_rule] = merge_value

    # add the merge rules back into the data
    data["mergeRule"] = rules_dict

    # build post request
    context = get_context()
    auth_token = context["authToken"]
    url = f'{context["endPoint"]}/{api_url}/lists/{list_name}/members'
    headers = {
        'Authorization': auth_token, 'Content-Type': 'application/json'
    }
    print(json.dumps(data))
    # make the request
    response = requests.post(url, data=json.dumps(data), headers=headers)
    # return the data to the container?
    data = rules["merge_or_update_members_in_a_profile_list_table"][0]
    return response


def get_member_of_list_by_riid(list_name, riid):
    """Retrieve a member of a profile list using RIID."""
    service_url = f'lists/{list_name}/members/{riid}'
    # only support returning all fields for now
    # TODO: implement other fields
    return get(service_url, parameters='fs=all')


def get_member_of_list_by_attribute(
    list_name,
    record_id,
    query_attribute='c',
    fields_to_return='all'
):
    """Retrieve a member of a profile list based on query attribute."""
    service_url = f'lists/{list_name}/members'
    parameters = f'fs={fields_to_return}&qa={query_attribute}&id={record_id}'
    return get(service_url, parameters=parameters)


def delete_from_profile_list(list_name, riid):
    """Delete Profile List Recipients based on RIID."""
    context = get_context()
    auth_token = context["authToken"]
    print(context["endPoint"])
    url = f'{context["endPoint"]}/{api_url}/lists/{list_name}/members/{riid}'
    headers = {'Authorization': auth_token}
    return requests.delete(url=url, headers=headers)


def get_profile_extensions(list_name):
    """Retrieve all profile extentions of a profile list."""
    return get(f'lists/{list_name}/listExtensions')


def create_profile_extension(
    list_name, fields='',
    folder_name='___api-generated',
    extension_name='_pet',
    default_field_type='STR500'
):
    """Create a new profile extension table."""
    extension_name = f'{list_name}{extension_name}'
    # field_types = ['STR500', 'STR4000', 'INTEGER', 'NUMBER', 'TIMESTAMP']
    data = {
        "profileExtension": {
            "objectName": extension_name,
            "folderName": folder_name
        }
    }
    # TODO: override default field type with fields from input list
    if fields != '':
        data["profileExtension"]["fields"] = [
            {
                "fieldName": field,
                "fieldType": default_field_type
            } for field in fields
        ]
    context = get_context()
    auth_token = context["authToken"]
    endpoint = f'{context["endPoint"]}/{api_url}/lists/{list_name}/listExtensions'
    headers = {'Authorization': auth_token, 'Content-Type': 'application/json'}
    return requests.post(url=endpoint, headers=headers)


# TODO: Merge or update members in a profile extension table
# extend/based on merge_or_update_members_in_a_profile_list_table
# def merge_or_update_members_in_a_profile_extension_table():
    # return
# Or use a more sensible name
# def profile_list_manage():
    # return merge_or_update_members_in_a_profile_extension_table()


def get_member_of_profile_extension_by_riid(
    list_name,
    profile_extension_name,
    riid,
    fields_to_return='all'
):
    """Retrieve a member of a profile extension table based on RIID."""
    return get(
        f'lists/{list_name}/listExtensions/{profile_extension_name}/members/{riid}',
        parameters=f'fs={fields_to_return}'
    )


def get_member_of_profile_extension_by_attribute(
    list_name,
    profile_extension_name,
    record_id,
    query_attribute='c',
    fields_to_return='all'
):
    """Retrieve a member of a profile extension table based on a query attribute."""

    service_url = f'lists/{list_name}/listExtensions/{profile_extension_name}/members'
    return get(
        service_url,
        parameters=f'fs={fields_to_return}&qa={query_attribute}&id={record_id}'
    )


def delete_member_of_profile_extension_by_riid(
    list_name,
    profile_extension_name,
    riid
):
    """Delete a member of a profile extension table based on RIID."""
    context = get_context()
    auth_token = context["authToken"]
    url = f'{context["endPoint"]}/{api_url}/lists/{list_name}/listExtensions/{profile_extension_name}/members/{riid}'
    headers = {'Authorization': auth_token}
    return requests.delete(url=url, headers=headers)


def create_supplemental_table(
    supplemental_table_name,
    folder_name,
    fields='',
    default_field_type='STR500',
    data_extraction_key=None,
    primary_key=None
):
    """Create a new supplemental table."""
    context = get_context()
    auth_token = context["authToken"]
    if type(fields) == str:
        raise TypeError('Fields must be a list.')
    url = f'{context["endPoint"]}/{api_url}/folders/{folder_name}/suppData'
    if primary_key is None:
        try:
            primary_key = fields[0]
        except:
            raise ValueError(
                """Cannot create supplemental table with no fields.
                Primary key field is required.""")
    data = {
        # TODO: Use field types per field
        "table": {"objectName": supplemental_table_name},
        "fields": [
            {
                "fieldName": field,
                "fieldType": default_field_type,
                "dataExtractionKey": False
            } for field in fields
        ],
        "primaryKeys": [primary_key]
    }
    headers = {'Authorization': auth_token, 'Content-Type': 'application/json'}
    return requests.post(url=url, headers=headers, data=json.dumps(data))


# def retrieve_supplemental_table_records_with_primary_key(
#     supplemental_table_name,
# ):
#     return


##################
# Extra features #
##################


def get_lists_for_record(riid):
    """Find what lists a record is in by RIID."""
    all_lists = [list_name["name"] for list_name in profile_lists()]
    # container list
    member_of = []
    for profile_list in all_lists:
        response = retrieve_a_member_of_a_profile_list_using_riid(
            profile_list,
            riid
        )
        # if the member (by riid) is in the profile list
        # add it to the list of all profile lists
        if "recordData" in response:
            member_of.append(profile_list)
    return member_of
