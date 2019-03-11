"""Tests for the internal classes, methods and functions."""
import pytest
import responsysrest as r

def test_credentials_no_args():
    # Test that the credentials class type errors when no arguments provided.
    with pytest.raises(Exception) as e_info:
        credentials = r.Credentials()


def test_credentials_with_args():
    # Test that the credentials class instantiates with args
    user_name = 'test_user_name'
    password = 'test_pass_word'
    email_address = 'email_address@email_address.biz'
    assert r.Credentials(user_name, password, email_address)


def test_from_json_on_nonbinary_path():
    # Test that the from json won't freak out with escape-looking backslash paths
    path = b'\mypath\'
    from_json = r.Credentials.from_json(path)
    assert from_json
