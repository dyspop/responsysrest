# Responsys Interact REST API python client #

A python library providing access to the Responsys Interact API. Currently supports version 1.3 Release 6.33 E65150-15.

## Install ##

Via source package:

    cd responsysrest/
    pip install .

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

r.login_with_username_and_password(r.secrets["user_name"], r.secrets["password"])
```

There are multiple ways of calling any part of the API.

### The documentation way:

Any function in the Responsys documentation (6.33 E65150-15) is created as a function name based on its documented name.

```
r.retrieve_all_profile_lists()
r.get_all_emd_email_campaigns()
```

### The better-named-than-the-documentation way.

Most of the names in the Responsys documentation are verbose. This client wrapper provides shorter, more sensible names.

```
r.profile_lists()
r.campaigns()
```

### The direct get

This wrapper library is constructed mostly on issuing requests in a format that the Interact API expects. As such you may call the get function directly to a desired endpoint:

```
r.get('lists')
r.get('campaigns')
```

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
