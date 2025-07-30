"""
AuthFi API - Python wrapper for Authentrend AuthFi WebAuthn/FIDO2 API

A comprehensive Python client for the Authentrend AuthFi API, providing
easy-to-use methods for WebAuthn/FIDO2 authentication, registration, and
user management.
"""

from .api import AuthFiApi, AuthfiApiEntity
from .utils import get_message

__version__ = "0.0.1"
__author__ = "Chumicat"
__email__ = "russell57260620@gmail.com"
__description__ = "Python wrapper for Authentrend AuthFi WebAuthn/FIDO2 API"

__all__ = [
    "AuthFiApi",
    "AuthfiApiEntity", 
    "get_message"
]
