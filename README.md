# Responsys Interact REST API python client #

A python library providing access to the Responsys Interact API. Currently supports version 1.3 Release 6.33 E65150-15.





## Install ##

1. Install Python3 and Python Package Index. 
  * OS X: It is recommended to install Python3 this way: http://docs.python-guide.org/en/latest/starting/install3/osx/ which should alias your Python3 to separate command `python3`.
2. Clone this repo and install via source package:
```
    cd responsysrest/
    pip install .
```

## Development Install

1. Clone this repo and install via source package in edit mode:
```
    cd responsysrest/
    pip install -e .
```


## Usage ##

1. Import Responsys Rest
2. Add credentials (for cli-mode)
3. Configure Interact connection settings
4. Get context from Interact remote
5. Use client

```
import responsysrest as r
creds = r.config.Credentials(mode='cli')
interact = r.config.Interact()
context = r.get_context(creds.user_name, creds.password, interact.login_url)

```

Now you are ready to go!

`mode='cli'` will prompt you for your credentials with `getpass`, but you can of course instead pass your credentials from some other context (directly, a locally loaded file, or an application) if you don't want to use the wrapper like a cli.

Interact will configure automatically as the following:

| Property  | Value  |
|---|---|
| pod  | 5  |
| api_folder  | ___api-generated  |
| api_list  | ___api-list  |
| profile_extension_table_alias  | _pet  |
| supplemental_table_alias  | _supp  |
| primary_key_alias  | _primary_key  |
| riid_generator_length  | 11  |
| test_campaign_name  | ___api-testing-campaign  |
| content_library_folder  | ___api-generated-cl  |
| api_version  | 1.3  |

Passing them in will instantiate Interact configuration differently, but other than the pod these are recommended settings. 

    interact = r.config.Interact(pod='2')


## Specific functions usage:



### Authenticating


#### Login with username and password

This can be called individually but isn't necessary since any function that requires it will call it.

    r.login(user_name, password)

The login itself returns a context with the Interact supplied endpoint for further requests for that user, an auth token, and a timestamp. Typically this is passed to whatever other request you make each time you do so.


#### Login with username and certificates

Not implemented.


#### Refresh token

Not implemented.



### Managing Profile List Tables


#### Retrieving all profile lists for an account

    r.get_profile_lists()
  
Returns a list of dictionaries of all profile lists. This comes bundled with the folder location and all of the field names too, so to retrieve just a list of the lists, or a list of the lists with their respective folders use

    [list["name"] for list in r.get_profile_lists()] 
    [(list["name"], list["folderName"]) for list in r.get_profile_lists()]


#### Merge or update members in a profile list table

Not implemented.


#### Retrieve a member of a profile list using RIID

    r.get_member_of_list_by_riid(list_name, riid)

Returns a full record if it's in the list.


#### Retrieve a member of a profile list based on query attribute

    r.get_member_of_list_by_id(list_name, record_id, query_attribute, fields_to_return)

Takes four arguments, but requires `list_name` and `record_id`. The list name is that which you want to find the record from in your Responsys Interact instance. The record id is the specific id you wish to use to identify the record. The query attribute is the type of id that you are using to retreive the record. The available options are `r` for RIID, `e` for EMAIL_ADDRESS, `c` for CUSTOMER_ID and `m` for MOBILE_NUMBER. The fields to return is a comma-separated list of the fields in the list, if left blank it will return all the fields.

Examples:

    r.get_member_of_list_by_id('CONTACTS_LIST', 'a@b.c')
    r.get_member_of_list_by_id('AFFILIATES', '901210', 'c', 'email_address_,first_name')


#### Delete Profile List Recipients based on RIID

    r.delete_from_profile_list(list_name, riid)

Examples:

    r.delete_from_profile_list('CONTACTS_LIST', 'a@b.c')




### Managing Profile Extension Tables


#### Retrieve all profile extentions of a profile list

    r.get_profile_extensions(list_name)

Returns the profile extension tables (also known as profile extensions, profile extenion lists, or PETs) associated with a given list. This comes bundled with the folder location and all of the field names too, so to retrieve just a list of the lists, or a list of the lists with their respective folders use:

    [list['profileExtension']['objectName'] for list in r.get_profile_extensions(list_name')]
    [(list['profileExtension']['objectName'], list['profileExtension']['folderName']) for list in r.get_profile_extensions(list_name)]


#### Create a new profile extension table

Creates a new profile extension table. Requires only the list name you wish to extend, but this will create a blank profile extension table using default a folder locations and name.

    r.create_profile_extension(list_name)

Examples:

    r.create_profile_extension('CONTACTS_LIST')

This creates a `CONTACTS_LIST_pet` profile extension table extending `CONTACTS_LIST` in a folder named `___api-generated` with no records and no non-default fields.

You can also specify the extension you want to use, but this function is slightly opinionated and will only let you create a profile extension table that begins with the name of the profile list that is being extended.

This example will create an empty profile extension table extending `CONTACTS_LIST` called `CONTACTS_LIST-Profile_Extension`:

    r.create_profile_extension('CONTACTS_LIST', extension_name='-Profile_Extension')

You can specify the folder to place it in as `___api-generated` isn't particularly likely to suit your needs:

    r.create_profile_extension('CONTACTS_LIST', folder_name='TestFolder')

Additionally you can supply fields as a list:

    r.create_profile_extension('CONTACTS_LIST', fields=['LTV_v1', 'LTV_v2', 'decile'])

If you don't specify a (Responsys Interact) data type for each it will default to `STR4000`. This default data type can be overridden with one of `STR500`, `STR4000`, `INTEGER`, `NUMBER`, or `TIMESTAMP`:

    r.create_profile_extension('CONTACTS_LIST', fields=['last_purchased_date', 'first_purchased_date'], default_field_type='TIMESTAMP')

You can also specify the field type of each within the list if you supply it as a list or tuple:

    r.create_profile_extension('CONTACTS_LIST', fields=[('last_purchased_date','TIMESTAMP'),('lifetime_purchases', 'INTEGER')])

The default field type override can be supplied alongside individual fields without their own field type specifications:

    r.create_profile_extension('CONTACTS_LIST', fields=[('probability_of_login', 'NUMBER'), 'CUSTOMER_ID_', ('ARTICLE_CONTENTS','STR4000')], default_field_type='STR500')


#### Merge or update members in a profile extension table

Not implemented.


#### Retrieve a member of a profile extension table based on RIID

Returns a full record if it's in the profile extension table.

    r.get_member_of_profile_extension_by_riid(list_name, pet_name, riid)

Also takes an optional argument `fields_to_return` which defaults to `all` if not specified. Examples:

    r.get_member_of_profile_extension_by_riid('CONTACTS_LIST', 'CONTACTS_LIST_pet', '101234567890')
    r.get_member_of_profile_extension_by_riid('CONTACTS_LIST', 'CONTACTS_LIST_pet', '101234567890', fields_to_return='FIRST_NAME, LAST_PURCHASE_DATE')


#### Retrieve a member of a profile extension table based on a query attribute

    r.get_member_of_profile_extension_by_attribute(list_name, pet_name record_id, query_attribute, fields_to_return)

Takes five arguments, but requires `list_name`, `pet_name` and `record_id`. The list name is that which you want to find the record from in your Responsys Interact instance. The record id is the specific id you wish to use to identify the record. The query attribute is the type of id that you are using to retreive the record. The available options are `r` for RIID, `e` for EMAIL_ADDRESS, `c` for CUSTOMER_ID and `m` for MOBILE_NUMBER. The fields to return is a comma-separated list of the fields in the list, if left blank it will return all the fields.

Examples:

    r.get_member_of_profile_extension_by_attribute('AFFILIATES', '901210', 'c', 'email_address_,first_name')


#### Delete a member of a profile extension table based on RIID

Deletes a member of a profile extension table based on RIID if it exists.

    r.delete_member_of_profile_extension_by_riid(list_name, pet_name, riid):



### Managing Supplemental Tables


#### Create a new supplemental table


Creates a new supplemental table. Requires only a table name, but this will create a blank supplemental table using default a folder location and name.

Examples:

    r.create_supplemental_table('CONTACTS_LIST', folder_name='test', fields=fields)

This creates a `CONTACTS_LIST_supp` supplemental table in a folder named `___api-generated` with no records and no non-default fields. You must specify either a list of at least one field or a primary key that is one of the Responsys internal field names. If you do not specify a primary key the wrapper will use the first field in the input list. This is because the API requires a primary key field. You can also specify an optional data extraction key.

    r.create_supplemental_table(supplemental_table_name, folder_name, fields=fields)
    r.create_supplemental_table(supplemental_table_name, folder_name, primary_key=primary_key)

The wrapper writes all fields with a default field type, which is `STR500` unless another type is specified. If the default type is specified it will use that type for all fields.

Examples:

    r.create_supplemental_table('my_supp_table', 'API_testing', fields=['field1', 'field2'], default_field_type='STR25', data_extraction_key='field2', primary_key='field1')




### Managing Campaigns


#### Get all EMD Campaigns

    r.get_campaigns()

Returns a dictionary of campaigns and their data, along with links and their data.

To see a list of all campaigns or a list of campaigns and their respective folders use:

    [campaign['name'] for campaign in r.get_campaigns()['campaigns']]
    [(campaign['name'], campaign['folderName']) for campaign in r.get_campaigns()['campaigns']]


#### Get all Push Campaigns

    r.get_push_campaigns()

Returns a list of push campaigns and their associated data.


### Managing Content


#### Create Folder

Creates a folder in the content library (`/contentlibary/`).

    r.create_folder('new_folder')

Creates a folder `/contentlibarary/new_folder` in the Content Library.

If you don't specify a folder the wrapper will default to the API folder name set in the user configuration `config.py`. By default that is `___api-generated` but can be changed. 




### Non-native features

There are a few things you might want to do with the API that are a little hard based on arbitrary endpoint calls. The wrapper provides you this piece of candy.


#### Get lists for record

    r.get_lists_for_record(riid)

Loops through every list and checks to see if the record is in the list. If the record is in the list it adds it to the returned object. This is very slow.



## Development/Testing ##

To run configuration and integration tests:

    $python3 -m pytest tests/

To run configuration tests only:

    $pytest tests/test_0dev_configs.py

To run client/API integration tests only:

    $pytest tests/test_2client.py

To run extra features tests only:

    $pytest tests/test_3extras.py

To run tests against the installed package distribution:

    $pytest

## Acknowledgements ##

This library was developed inspired by the SOAP client on pypi as ```responsys```. 
🙇 Oracle for the heavy lifting building and maintaining their API.

## Legal ##

This code is neither officially supported nor endorsed by Oracle, Responsys, or any related entities.
