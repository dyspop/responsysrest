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

Call `dir(r)` to see a list of all possible functions.


## Development/Testing ##

Tests can be run via setuptools:

    python setup.py nosetests

Testing within a dev environment can be accomplished via ```nosetests```.

## Acknowledgements ##

This library was developed inspired by the SOAP client on pypi as ```responsys```. 
🙇 Oracle for the heavy lifting building and maintaining their API.

## Legal ##

This code is neither officially supported nor endorsed by Oracle, Responsys, or any related entites.
