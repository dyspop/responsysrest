import os
import json
from dataclasses import dataclass

@dataclass
class Credentials:
    """Load credentials information like passwords."""

    user_name: str
    password: str
    email_address: str
    certificates: None = None


def from_json(f: bytes):
    """Load credentials from json."""
    with open(bytes(f)) as f:
        user_secrets = json.load(f)
        creds = Credentials(
            user_name=user_secrets['user_name'],
            password=user_secrets['password'],
            email_address=user_secrets['email_address'])
        return creds


def auto():
    """Look for the secret.json file."""
    # traverse root directory looking for credentials
    for root, dirs, files in os.walk("."):
        for f in files:
            if f == 'secret.json':
                try:
                    return from_json(f)
                except(ValueError):
                    raise ValueError('Could not open {f}'.format(f=f))
                break
