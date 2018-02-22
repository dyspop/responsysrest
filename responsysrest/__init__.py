"""Python client library for the Responsys Interact REST API."""

from .client import Client
from .containers import rules
from .configuration import Configuration
from .configuration import configuration.auto
from .credentials import Credentials
from .credentials import credentials.auto

__version__ = "0.1.0"
__keywords__ = "responsys interact client rest api"
