"""Python client library for the Responsys Interact REST API."""

from .client import Client
from .containers import rules
from .configuration import Configuration
from .credentials import Credentials, auto

__version__ = "0.1.0"
__keywords__ = "responsys interact client rest api"
