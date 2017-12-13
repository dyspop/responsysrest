"""Tests for each individual function in the Client."""
import responsysrest as r

# import with two names for grammar purposes.
from secret import secrets as secret, secrets


def test_secrets():
    """Test to see if our secrets are stored."""
    for key in secrets:
        assert secret[key] is not None
        assert secret[key] != ''


def test_profile_lists():
    """Test to see if profile lists has data."""
    # TODO: what happens if there are no lists defined in Interact?
    assert len(r.profile_lists()) > 0
