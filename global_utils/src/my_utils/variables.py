"""
Global Variables that can be used across different projects.
It uses .env for credentials and sensitive data.
"""

from decouple import config
import pytest
from .string_converters import convert_string_to_bool

# pytest.environment is configured in the conftest.py
CURRENT_ENVI = None
try:
    CURRENT_ENVI = pytest.environment
except AttributeError:
    print("Running Unittest for Global Utils. Setting CURRENT_ENVI to default 'STAGING'.")
    CURRENT_ENVI = "STAGING"

API_DEBUG_MODE = convert_string_to_bool(config("API_DEBUG_MODE"))

# From .env Test Account Details
TEST_ACCOUNT_EMAIL = config(f"{CURRENT_ENVI.upper()}_TEST_ACCOUNT_EMAIL")
TEST_ACCOUNT_PASSWORD = config(f"{CURRENT_ENVI.upper()}_TEST_ACCOUNT_PASSWORD")

# From .env config URL's
DOMAIN = config(f"{CURRENT_ENVI}_API_HOST") + config(f"{CURRENT_ENVI}_API_VERSION")

# Bearer Token that can be found after successful login
ACCOUNT_TOKEN = config(f"{CURRENT_ENVI}_TEST_ACCOUNT_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {ACCOUNT_TOKEN}"
}
