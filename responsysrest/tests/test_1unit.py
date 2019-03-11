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


def test_from_json_on_windows_path():
    # Test that the from json won't freak out with escape-looking backslash paths
    path = b'C:\\Users\\randomuser\\paththatshould not exist\\Application\\Sub Directory\\config.json'
    with pytest.raises(Exception) as e_info:
        from_json = r.credentials.from_json(path)
