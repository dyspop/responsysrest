"""Tests for the internal classes, methods and functions."""
import pytest
import responsysrest as r

def test_credentials_no_args():
    # Test that the credentials class type errors when no arguments provided.
    with pytest.raises(Exception) as e_info:
        credentials = r.Credentials()
