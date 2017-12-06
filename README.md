# Responsys Interact REST API python client #

A python library providing access to the Responsys Interact API. Currently supports version 1.3 Release 6.33 E65150-15.

## Install ##

You can install this other ways, but I recommend installing Python3 this way:
http://docs.python-guide.org/en/latest/starting/install3/osx/

This should alias your Python3 and pip to separate commands `python3` and `pip3`.

Then you can clone this repo and install via source package:

    cd responsysrest/
    pip3 install .

## Usage ##

Set your username and password as a dictionary data object in `responsysrest/secret.py`
IMPORTANT: this is ignored by git. If you use another version control you'll need to keep this file out of the way from it!

```
secrets = {
    "user_name" : "MyResponsysInteractAPIuserName",
    "password" : "FillInPasswordHere"
}
```

If you were to need to set these manually you'd do it like this:

```
import responsysrest as r

username = r.secrets["user_name"]
password = r.secrets["password"]
r.login(username, password)
```

In general you should not need to call login from a single user command line session. If you are using this API wrapper to build an application on top of the Interact API then the login function is available to you, but it's still probably not as good as calling the API ad-hoc in order to issue context for the call. The wrapper should manage refreshing context for you.

---

There are multiple ways of calling any part of the API.

### Documentation Style

Any function in the Responsys documentation (6.33 E65150-15) is created as a function name based on its documented name.

```
r.retrieve_all_profile_lists()
r.get_all_emd_email_campaigns()
```

### Better Style

Most of the names in the Responsys documentation are verbose. This client wrapper provides shorter, more sensible names.

```
r.profile_lists()
r.campaigns()
```

### CRUD Style

This wrapper library is constructed mostly on issuing requests in a format that the Interact API expects. As such you may call the get function directly to a desired endpoint:

```
r.get('lists')
r.get('campaigns')
```

### Complete usage mapping:
| English  | Documentation  | Better  | CRUD  |
|---    |---    |---    |---    |
| Login with username and password      | `login_with_username_and_password(user_name, password)`      | `login(user_name, password)`       | n/a      |
| Retrieving all profile lists for an account      | `retrieving_all_profile_lists_for_an_account()`      | `profile_lists()`      | `get('lists')`      |
| Get all EMD email campaigns      | `get_all_emd_email_campaigns()`      | `campaigns()`      | `get('campaigns')`      |
| Merge or update members in a profile list table      | `merge_or_update_members_in_a_profile_list_table(list)`      | `list_manage(list_name)`      | n/a      |
| Retrieve a member of a profile list using RIID      | `retrieve_a_member_of_a_profile_list_using_riid(list_name, riid)`      | `get_member_of_list_by_riid(list_name, riid)` | n/a     |
| Retrieve a member of a profile list based on query attribute      | `retrieve_a_member_of_a_profile_list_based_on_query_attribute(list_name, record_id, query_attribute, fields_to_return)`       | `get_member_of_list_by_id(list_name, record_id, query_attribute, fields_to_return)` | `get(f'lists/{list_name}/members/', parameters=f'fs={fields_to_return}&qa={query_attribute}&id={record_id}')`    |
| Delete Profile List Recipients based on RIID      | `r.delete_profile_list_recipients_based_on_riid(list_name, riid)`       | `r.delete_from_profile_list(list_name, riid)` | n/a    |
| Get lists for record      | n/a       | `get_lists_for_record(riid)` | n/a    |
| Retrieve all profile extentions of a profile list      | `retrieve_all_profile_extensions_of_a_profile_list(list_name)`       | `get_profile_extensions(list_name)` | `get(f'lists/{list_name}/listExtensions'`    |

### Specific functions usage:

#### Login with username and password

This can be called individually but isn't necessary since any function that requires it will call it.

    r.login_with_username_and_password(user_name, password)

or

    r.login(user_name, password)

The login itself returns a context with the Interact supplied endpoint for further requests for that user, an auth token, and a timestamp. Typically this is passed to whatever other request you make each time you do so.

#### Retrieving all profile lists for an account

    r.retrieving_all_profile_lists_for_an_account()

or

    r.profile_lists()

or
    
    r.get('lists')

Returns a list of dictionaries of all profile lists. This comes bundled with the folder location and all of the field names too, so to retrieve just a list of the lists, or a list of the lists with their respective folders use

    [list["name"] for list in r.profile_lists()] 
    [(list["name"], list["folderName"]) for list in r.profile_lists()]

#### Get all EMD Campaigns

    r.get_all_emd_email_campaigns()

    r.campaigns()

Returns a dictionary of campaigns and their data, along with links and their data. To see a list of all campaigns or a list of campaigns and their respective folders use

    [campaign['name'] for campaign in r.campaigns()['campaigns']]
    [(campaign['name'], campaign['folderName']) for campaign in r.campaigns()['campaigns']]

#### Retrieve a member of a profile list using RIID

    r.retrieve_a_member_of_a_profile_list_using_riid(list_name, riid)

or

    r.get_member_of_list_by_riid(list_name, riid)

Returns a full record if it's in the list.

#### Retrieve a member of a profile list based on query attribute

    r.retrieve_a_member_of_a_profile_list_based_on_query_attribute(list_name, record_id, query_attribute, fields_to_return)

or

    r.get_member_of_list_by_id(list_name, record_id, query_attribute, fields_to_return)

or

    r.get('lists/{list_name}/members/', parameters=f'fs={fields_to_return}&qa={query_attribute}&id={record_id}')

Takes four arguments, but requires list name and record id. The list name is that which you want to find the record from in your Responsys Interact instance. The record id is the specific id you wish to use to identify the record. The query attribute is the type of id that you are using to retreive the record. The available options are `r` for RIID, `e` for EMAIL_ADDRESS, `c` for CUSTOMER_ID and `m` for MOBILE_NUMBER. The fields to return is a comma-separated list of the fields in the list, if left blank it will return all the fields.

Examples:

    r.get_member_of_list_by_id('CONTACTS_LIST', 'a@b.c')
    r.get_member_of_list_by_id('AFFILIATES', '901210', 'c', 'email_address_,first_name')

#### Delete Profile List Recipients based on RIID

    r.delete_profile_list_recipients_based_on_riid(list_name, riid)

or

    r.delete_from_profile_list(list_name, riid)

Examples:

    r.delete_from_profile_list('CONTACTS_LIST', 'a@b.c')

#### Retrieve all profile extentions of a profile list

    r.retrieve_all_profile_extensions_of_a_profile_list(list_name)

or

    r.get_profile_extensions(list_name)

or

    r.get(f'lists/{list_name}/listExtensions')

Returns the profile extension tables (also known as profile extensions, profile extenion lists, or PETs) associated with a given list. This comes bundled with the folder location and all of the field names too, so to retrieve just a list of the lists, or a list of the lists with their respective folders use

    [list['profileExtension']['objectName'] for list in r.get_profile_extensions(list_name')]
    [(list['profileExtension']['objectName'], list['profileExtension']['folderName']) for list in r.get_profile_extensions(list_name)]

#### Get lists for record

    r.get_lists_for_record(riid)

Loops through every list and checks to see if the record is in the list. If the record is in the list it adds it to the returned object. This is very slow.

####

## Development/Testing ##

None!

## Acknowledgements ##

This library was developed inspired by the SOAP client on pypi as ```responsys```. 
🙇 Oracle for the heavy lifting building and maintaining their API.

## Legal ##

This code is neither officially supported nor endorsed by Oracle, Responsys, or any related entities.
