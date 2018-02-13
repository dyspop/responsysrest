"""Responsys REST API Client."""
# used to issue CRUD requests, the meat and 'taters of this thing
import requests

# used with the login with certificate functions
# import base64 as base64

# Interact API returns a lot of json-like text objects
# we use this to bind them to python objects
import json
# For stripping comments from our json
from jsmin import jsmin

# used with the login with certificate functions
# from random import choice

# used with the login with certificate functions
# from string import ascii_uppercase

# connector config
import config
from config import pod

# this should get removed, but can be used to store a local password!
# crazy... but Interact has additional security measures
# on top of your user login / password and these aren't stored
# anywhere else than your local machine or app server.
# If you can encrypt/decrypt them yourself... please do!
# TODO: proper password prompting/storage
from secret import secrets as secret
# our own rules for data objects.
from .containers import rules

api_url = 'rest/api/v1.3'
login_url = f'http://login{pod}.responsys.net/{api_url}/'

# Helper functions for use with direct implementations of calls as below

# # Helps with Login with username and certificates
# def generate_client_challenge_value(length=16):
#     return base64.b64encode(
#         bytes(''.join(choice(ascii_uppercase) for i in range(16)), 'utf-8')
#     )


class Configuration:
    """How our client is configured."""

    def __init__(
            self,
            pod='5',
            api_folder='___api-generated',
            api_list='API_testing',
            profile_extension_table_alias='_pet',
            supplemental_table_alias='_supp',
            primary_key_alias='_primary_key',
            riid_generator_length=11,
            test_email_address='',
            test_campaign_name='',
            test_content_library_folder=''
    ):
        """Initialize the Configuration."""
        self.pod = pod
        self.api_folder = api_folder
        self.api_list = api_list
        self.profile_extension_table_alias = profile_extension_table_alias
        self.supplemental_table_alias = supplemental_table_alias
        self.primary_key_alias = primary_key_alias
        self.riid_generator_length = riid_generator_length
        self.test_email_address = test_email_address
        self.test_campaign_name = test_campaign_name
        self.test_content_library_folder = test_content_library_folder

    def __get_config(self):
        """Get data from the config file."""
        with open("config.json", "r") as f:
            raw = f.read()
            minified = jsmin(raw)
            data = json.loads(minified)[0]

    @property
    def pod(self):
        """Get pod."""
        return self.__pod

    @pod.setter
    def pod(self, pod):
        """Set the pod.

        Only known pods are 2 and 5.
        """
        if str(int(pod)) in ['2', '5']:
            self.__pod = pod
        else:
            raise ValueError('Only pods 2 and 5 are supported.')

    @property
    def api_folder(self):
        """Get API folder."""
        return self.__api_folder

    @api_folder.setter
    def api_folder(self, api_folder):
        """Set the API folder."""
        self.__api_folder = api_folder

    @property
    def api_list(self):
        """Get API list."""
        return self.__api_list

    @api_list.setter
    def api_list(self, api_list):
        """Set API list."""
        self.__api_list = api_list

    @property
    def profile_extension_table_alias(self):
        """Get profile extension table alias."""
        return self.__profile_extension_table_alias

    @profile_extension_table_alias.setter
    def profile_extension_table_alias(self, profile_extension_table_alias):
        """Set profile extension table alias."""
        self.__profile_extension_table_alias = profile_extension_table_alias

    @property
    def supplemental_table_alias(self):
        """Get supplemental table alias."""
        return self.__supplemental_table_alias

    @supplemental_table_alias.setter
    def supplemental_table_alias(self, supplemental_table_alias):
        """Set supplemental table alias."""
        self.__supplemental_table_alias = supplemental_table_alias

    @property
    def primary_key_alias(self):
        """Get primary key alias."""
        return self.__primary_key_alias

    @primary_key_alias.setter
    def primary_key_alias(self, primary_key_alias):
        """Set primary key alias."""
        self.__primary_key_alias = primary_key_alias

    @property
    def riid_generator_length(self):
        """Get riid generator length."""
        return self.__riid_generator_length

    @riid_generator_length.setter
    def riid_generator_length(self, riid_generator_length):
        """Set riid generator length."""
        self.__riid_generator_length = riid_generator_length

    @property
    def test_email_address(self):
        """Get test email address."""
        return self.__test_email_address

    @test_email_address.setter
    def test_email_address(self, test_email_address):
        """Set test email address."""
        self.__test_email_address = test_email_address

    @property
    def test_campaign_name(self):
        """Get test campaign name."""
        return self.__test_campaign_name

    @test_campaign_name.setter
    def test_campaign_name(self, test_campaign_name):
        """Set test campaign name."""
        self.__test_campaign_name = test_campaign_name

    @property
    def test_content_library_folder(self):
        """Get test content library folder."""
        return self.__test_content_library_folder

    @test_content_library_folder.setter
    def test_content_library_folder(self, test_content_library_folder):
        """Set test content library folder."""
        self.__test_content_library_folder = test_content_library_folder



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


"""Direct implentations of calls from Responsys Interact REST API documentation
https://docs.oracle.com/cloud/latest/marketingcs_gs/OMCEB/OMCEB.pdf
All comment descriptions are directly from the v1.3 REST API documentation,
except some English-language grammar and syntax inconsistencies are modified
from their documentation and code-comment style to match PEP-8.
"""


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


def get_push_campaigns():
    """Get all Push campaigns."""
    return get('campaigns?type=push')


def send_email_message(email_address, folder_name, campaign_name):
    """Trigger email message."""
    data = {
        "recipientData": [
            {
                "recipient": {
                    "emailAddress": email_address,
                    "listName": {
                        "folderName": folder_name,
                        "objectName": campaign_name
                    },
                    "recipientId": None,
                    "mobileNumber": None,
                    "emailFormat": "HTML_FORMAT"
                }
            }
        ]
    }
    context = get_context()
    headers = {
        'Authorization': context["authToken"],
        'Content-Type': 'application/json'
    }
    url = f'{context["endPoint"]}/{api_url}/campaigns/{campaign_name}/email'
    return requests.post(data=json.dumps(data), headers=headers, url=url)


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
    """Retrieve all profile extensions of a profile list."""
    return get(f'lists/{list_name}/listExtensions')


def create_profile_extension(
    list_name, fields='',
    folder_name=config.api_folder,
    extension_name=config.profile_extension_table_alias,
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
    url = f'{context["endPoint"]}/{api_url}/lists/{list_name}/listExtensions'
    headers = {'Authorization': auth_token, 'Content-Type': 'application/json'}
    return requests.post(url=url, headers=headers)


# TODO: Merge or update members in a profile extension table
# extend/based on merge_or_update_members_in_a_profile_list_table
# def merge_or_update_members_in_a_profile_extension_table():
    # return
# Or use a more sensible name
# def profile_list_manage():
    # return merge_or_update_members_in_a_profile_extension_table()


def get_member_of_profile_extension_by_riid(
    list_name,
    pet_name,
    riid,
    fields_to_return='all'
):
    """Retrieve a member of a profile extension table based on RIID."""
    return get(
        f'lists/{list_name}/listExtensions/{pet_name}/members/{riid}',
        parameters=f'fs={fields_to_return}'
    )


def get_member_of_profile_extension_by_attribute(
    list_name,
    pet_name,
    record_id,
    query_attribute='c',
    fields_to_return='all'
):
    """Retrieve a member of a profile extension table
    based on a query attribute.
    """
    service_url = f'lists/{list_name}/listExtensions/{pet_name}/members'
    return get(
        service_url,
        parameters=f'fs={fields_to_return}&qa={query_attribute}&id={record_id}'
    )


def delete_member_of_profile_extension_by_riid(
    list_name,
    pet_name,
    riid
):
    """Delete a member of a profile extension table based on RIID."""
    context = get_context()
    auth_token = context["authToken"]
    endpoint = context["endPoint"]
    url = f'{endpoint}/{api_url}/lists/{list_name}/listExtensions/{pet_name}/members/{riid}'
    headers = {'Authorization': auth_token}
    return requests.delete(url=url, headers=headers)


def create_supplemental_table(
    supplemental_table_name,
    folder_name=config.api_folder,
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


def create_folder(folder_path=config.api_folder):
    """Create a new folder in /contentlibrary/."""
    context = get_context()
    auth_token = context["authToken"]
    endpoint = context["endPoint"]
    headers = {'Authorization': auth_token, 'Content-Type': 'application/json'}
    url = f'{endpoint}/{api_url}/clFolders/'
    data = {
        "folderPath": f'/contentlibrary/{folder_path}'
    }
    return requests.post(url=url, data=json.dumps(data), headers=headers)


def delete_folder(folder_path=config.api_folder):
    """Delete a folder in /contentlibrary/."""
    context = get_context()
    auth_token = context["authToken"]
    endpoint = context["endPoint"]
    headers = {'Authorization': auth_token }
    url = f'{endpoint}/{api_url}/clFolders/contentlibrary/{folder_path}'
    return requests.delete(url=url, headers=headers)


##################
# Extra features #
##################


def get_lists_for_record(riid):
    """Find what lists a record is in by RIID."""
    all_lists = [list_name["name"] for list_name in get_profile_lists()]
    # container list
    member_of = []
    for profile_list in all_lists:
        response = get_member_of_list_by_riid(profile_list, riid)
        # if the member (by riid) is in the profile list
        # add it to the list of all profile lists
        if "recordData" in response:
            member_of.append(profile_list)
    return member_of
