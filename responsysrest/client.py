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

# our own rules for data objects.
# from .containers import rules

# Helper functions for use with direct implementations of calls as below

# # Helps with Login with username and certificates
# def generate_client_challenge_value(length=16):
#     return base64.b64encode(
#         bytes(''.join(choice(ascii_uppercase) for i in range(16)), 'utf-8')
#     )


class Client:
    """The main client."""

    def __init__(self, config, creds):
        """Initialize."""
        self.config = config
        self.creds = creds

    def _login(self, user_name, password, url):
        """Login with username and password."""
        data = {
            "user_name": user_name,
            "password": password,
            "auth_type": "password"
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        return requests.post(url, data=data, headers=headers)

    def _get_context(self):
        """
        Return the login response as context.

        Used with each individual call to Responsys API.
        """
        context = json.loads(
            self._login(
                self.creds.user_name,
                self.creds.password,
                self.config.login_url
            ).text
        )
        context['api_url'] = self.config.api_url
        return context

    def _get(self, service_url, **kwargs):
        """General purpose build for GET requests to Interact API."""
        context = self._get_context()
        auth_token = context["authToken"]
        endpoint = f'{context["endPoint"]}/{context["api_url"]}/{service_url}'
        headers = kwargs.get('headers', {'Authorization': auth_token})
        # use parameters if we got them
        if "parameters" in kwargs:
            parameters = kwargs.get('parameters', None)
            endpoint = f'{endpoint}?{parameters}'
        response = requests.get(url=endpoint, headers=headers)
        response_object = json.loads(response.text)
        return response_object

    def _post(self, service_url, data, **kwargs):
        context = self._get_context()
        data = json.dumps(data)
        headers = {
            'Authorization': context["authToken"],
            'Content-Type': 'application/json'
        }
        endpoint = f'{context["endPoint"]}/{context["api_url"]}/{service_url}'
        response = requests.post(data=data, headers=headers, url=endpoint)
        response_object = json.loads(response.text)
        return response_object

    def _delete(self, service_url):
        context = self._get_context()
        headers = {'Authorization': context["authToken"]}
        endpoint = f'{context["endPoint"]}/{context["api_url"]}/{service_url}'
        response = requests.delete(url=endpoint, headers=headers)
        response_object = json.loads(response.text)
        return response_object

    def _trim_path(self, path):
        # chop trailing slash
        if path[-1] == '/':
            path = path[:-1]
        # chop leading slash
        if path[0] == '/':
            path = path[1:]
        return path

    """Direct implentations of calls from Responsys Interact REST API documentation
    https://docs.oracle.com/cloud/latest/marketingcs_gs/OMCEB/OMCEB.pdf
    All comment descriptions are directly from the v1.3 REST API documentation,
    except some English-language grammar and syntax inconsistencies are
    modified from their documentation and code-comment style to match PEP-8.
    """

    def get_profile_lists(self):
        """Retrieving all profile lists for an account."""
        return self._get('lists')

    def get_campaigns(self):
        """Get all EMD email campaigns."""
        return self._get('campaigns')

    def get_push_campaigns(self):
        """Get all Push campaigns."""
        return self._get('campaigns?type=push')

    def get_member_of_list_by_riid(
        self,
        list_name,
        riid,
        fields_to_return=['all']
    ):
        """Retrieve a member of a profile list using RIID."""
        service_url = f'lists/{list_name}/members/{riid}'
        parameters = f'fs={",".join(fields_to_return)}'
        return self._get(service_url, parameters=parameters)

    def get_member_of_list_by_attribute(
        self,
        list_name,
        record_id,
        query_attribute='c',
        fields_to_return=['all']
    ):
        """Retrieve a member of a profile list based on query attribute."""
        service_url = f'lists/{list_name}/members'
        parameters = f'fs={",".join(fields_to_return)}&qa={query_attribute}&id={record_id}'
        return self._get(service_url, parameters=parameters)

    def get_profile_extensions_for_list(self, list_name):
        """Retrieve all profile extensions of a profile list."""
        return self._get(f'lists/{list_name}/listExtensions')

    def get_member_of_profile_extension_by_riid(
        self,
        list_name,
        pet_name,
        riid,
        fields_to_return=['all']
    ):
        """Retrieve a member of a profile extension table based on RIID."""
        service_url = f'lists/{list_name}/listExtensions/{pet_name}/members/{riid}'
        parameters = f'fs={",".join(fields_to_return)}'
        return self._get(service_url, parameters=parameters)

    def get_member_of_profile_extension_by_attribute(
        self,
        list_name,
        pet_name,
        record_id,
        query_attribute='c',
        fields_to_return=['all']
    ):
        """Retrieve a member of a profile extension table based on a query attribute."""
        service_url = f'lists/{list_name}/listExtensions/{pet_name}/members'
        parameters = f'fs={",".join(fields_to_return)}&qa={query_attribute}&id={record_id}'
        return self._get(service_url, parameters=parameters)

    def get_lists_for_record(self, riid):
        """Find what lists a record is in by RIID."""
        all_lists = [list_name["name"] for list_name in self.get_profile_lists()]
        # container list
        member_of = []
        for profile_list in all_lists:
            response = self.get_member_of_list_by_riid(
                self, profile_list, riid)
            # if the member (by riid) is in the profile list
            # add it to the list of all profile lists
            if "recordData" in response:
                member_of.append(profile_list)
        return member_of

    def send_email_message(self, email_address, folder_name, campaign_name):
        """Trigger email message."""
        data = {
            "recipientData": [{
                "recipient": {
                    "emailAddress": email_address,
                    "listName": {
                        "folderName": folder_name,
                        "objectName": campaign_name},
                    "recipientId": None,
                    "mobileNumber": None,
                    "emailFormat": "HTML_FORMAT"}}]}  # Damn that's ugly
        service_url = f'campaigns/{campaign_name}/email'
        return self._post(service_url, data)

    def delete_from_profile_list(self, list_name, riid):
        """Delete Profile List Recipients based on RIID."""
        service_url = f'lists/{list_name}/members/{riid}'
        return self._delete(service_url)

    def delete_member_of_profile_extension_by_riid(
        self,
        list_name,
        pet_name,
        riid
    ):
        """Delete a member of a profile extension table based on RIID."""
        service_url = f'lists/{list_name}/listExtensions/{pet_name}/members/{riid}'
        return self._delete(service_url)

    def create_supplemental_table(
        self,
        supplemental_table_name,
        folder_name='',
        fields='',
        default_field_type='STR500',
        data_extraction_key=None,
        primary_key=None
    ):
        """Create a new supplemental table."""
        if type(fields) == str:
            raise TypeError('Fields must be a list.')
        if folder_name == '':
            folder_name = self.config.api_folder
        service_url = f'folders/{folder_name}/suppData'
        if primary_key is None:
            try:
                primary_key = fields[0]
            except ValueError:
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
        return self._post(service_url, data)

    def create_folder(self, folder_path=''):
        """Create a new folder in /contentlibrary/."""
        service_url = 'clFolders'
        if folder_path == '':
            folder_path = self.config.content_library_folder
        data = {
            "folderPath": f'/contentlibrary/{folder_path}'
        }
        return self._post(service_url, data)

    def delete_folder(self, folder_path=''):
        """Delete a folder in /contentlibrary/."""
        if folder_path == '':
            folder_path = self.config.content_library_folder
        service_url = f'clFolders/contentlibrary/{folder_path}'
        return self._delete(service_url)

    def create_document(self, document, sub_folder_path=None):
        """Create a document in /contentlibrary/."""
        if not sub_folder_path:
            sub_folder_path = self.config.content_library_folder
        path = self._trim_path(sub_folder_path)
        service_url = 'clDocs'
        document_data = open(document, 'r').read()
        # just use the filename, omit the path
        document_name = document.split('/')[-1]
        data = {
            'documentPath': f'/contentlibrary/{path}/{document_name}',
            'content': document_data
        }
        return self._post(service_url, data)

    def get_document(self, document, sub_folder_path=None):
        """Get a document from /contentlibrary/."""
        if sub_folder_path == None:
            sub_folder_path = self.config.content_library_folder
        service_url = f'clDocs/contentlibrary/{sub_folder_path}/{document}'
        return self._get(service_url)


    # TODO: fix client error
    # def create_profile_extension(
    #     self,
    #     list_name,
    #     fields='',
    #     folder_name='',
    #     extension_name='',
    #     default_field_type='STR500'
    # ):
    #     """Create a new profile extension table."""
    #     if folder_name == None or folder_name == '':
    #         folder_name = self.config.api_folder
    #     if extension_name == None or extension_name == '':
    #         extension_name = f'{list_name}{self.config.profile_extension_table_alias}'
    #     # field_types = ['STR500', 'STR4000', 'INTEGER', 'NUMBER', 'TIMESTAMP']
    #     data = {
    #         "profileExtension": {
    #             "objectName": extension_name,
    #             "folderName": folder_name
    #         }
    #     }
    #     # TODO: override default field type with fields from input list
    #     if fields != '':
    #         data["profileExtension"]["fields"] = [
    #             {
    #                 "fieldName": field,
    #                 "fieldType": default_field_type
    #             } for field in fields
    #         ]
    #     service_url = f'lists/{list_name}/listExtensions'
    #     return self._post(service_url, data)

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

# # Merge or update members in a profile list table
# # TODO: fix 403 response
# # TODO: implement context and api_url with post
# def manage_profile_list(list_name, **kwargs):
#     """Merge or update members in a profile list table."""
#     # load container data
#     data = rules["merge_or_update_members_in_a_profile_list_table"][0]
#     # process keyword arguments
#     fields = kwargs.get('fields')
#     records = kwargs.get('records', None)
#     merge_rules = kwargs.get('merge_rules', data["mergeRule"])

#     # make sure the input fields and records are lists
#     if isinstance(fields, list) and isinstance(records, list):
#         # make sure the fields and records have the same amount of columns
#         if len(fields) == len(records):
#             # insert our fields into the data
#             data["recordData"]["fieldNames"] = fields
#             # insert our records into the data
#             data["recordData"]["records"] = records
#         else:
#             raise ValueError(
#                 """ERROR: List headers count does not
#                 match record column count"""
#             )
#     else:
#         raise ValueError(
#             """
#             ARGUMENT ERROR: input fields or records are not list objects.\n
#             Please specify lists for 'fields' or 'records' arguments.
#             """
#         )
#     # extract merge rules
#     rules_keys = [key for key in data["mergeRule"]]
#     # extract merge rules default values
#     rules_values = [
#         data["mergeRule"][rule]["default"] for rule in rules_keys
#     ]
#     # assign a new rules object to work on before we insert it into the
#     # request object
#     rules_dict = dict(zip(rules_keys, rules_values))

#     for merge_rule, merge_value in merge_rules.items():
#         try:
#             # if the user input merge rule value is valid based on the
#             # container data
#             if merge_value in data["mergeRule"][merge_rule]["options"]:
#                 # add the new merge rule value to the data
#                 data["mergeRule"][merge_rule] = merge_value
#         except KeyError:
#             print(
#                 """
#                 f'ERROR: Merge rule "{merge_rule}" is not valid.
#                 Valid merge rules are:
#                 {rules_keys}'
#                 """
#             )
#         # print(merge_rule + " : " + merge_value)
#         # assign parameters from merge_rules keyword arguments to new rules
#         rules_dict[merge_rule] = merge_value

#     # add the merge rules back into the data
#     data["mergeRule"] = rules_dict

#     # build post request
#     context = get_context()
#     auth_token = context["authToken"]
#     url = f'{context["endPoint"]}/{api_url}/lists/{list_name}/members'
#     headers = {
#         'Authorization': auth_token, 'Content-Type': 'application/json'
#     }
#     print(json.dumps(data))
#     # make the request
#     response = requests.post(url, data=json.dumps(data), headers=headers)
#     # return the data to the container?
#     data = rules["merge_or_update_members_in_a_profile_list_table"][0]
#     return response

# TODO: Merge or update members in a profile extension table
# extend/based on merge_or_update_members_in_a_profile_list_table
# def merge_or_update_members_in_a_profile_extension_table():
    # return
# Or use a more sensible name
# def profile_list_manage():
    # return merge_or_update_members_in_a_profile_extension_table()
