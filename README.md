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

```
import responsysrest as r

username = r.secrets["user_name"]
password = r.secrets["password"]
r.login(username, password)
```

In general you should not need to call login from a single user command line session. If you are using this API wrapper to build an application on top of the Interact API then the login function is available to you, but it's still probably not as good as calling the API ad-hoc in order to issue context for the call. The wrapper should manage refreshing context for you.

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


This wrapper is opinionated and returns a json object where appropriate rather than the raw string.

## Development/Testing ##

Tests can be run via setuptools:

    python setup.py nosetests

Testing within a dev environment can be accomplished via ```nosetests```.

## Acknowledgements ##

This library was developed inspired by the SOAP client on pypi as ```responsys```. 
🙇 Oracle for the heavy lifting building and maintaining their API.

## Legal ##

This code is neither officially supported nor endorsed by Oracle, Responsys, or any related entites.
