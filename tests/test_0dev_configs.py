"""Test development configuration."""
from secret import secrets as secret


def test_import_secrets():
    """Test everything the secrets, the user may not have added them."""
    for k in secret:
        assert None is not secret[k]
        assert '' != secret[k]
