"""
Terrakio API Client

A Python client for accessing Terrakio's Web Coverage Service (WCS) API.
"""

__version__ = "0.3.3"

from terrakio_core.client import BaseClient
from terrakio_core.config import create_default_config
from terrakio_core.exceptions import APIError, ConfigurationError, DownloadError, ValidationError
from terrakio_core.user_management import UserManagement

class Client(BaseClient):
    """Terrakio API client for regular users."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_admin = False

__all__ = [
    'Client',
    'create_default_config',
    'APIError',
    'ConfigurationError',
    'DownloadError',
    'ValidationError',
    'UserManagement',
]