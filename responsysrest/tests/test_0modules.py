# Tests for loading python modules.

from importlib import util as import_util


# Test that the requirements modules load

def test_requirement_certifi():
    """Test that certifi is found."""
    assert None is not import_util.find_spec('certifi')

def test_requirement_chardet():
    """Test that chardet is found."""
    assert None is not import_util.find_spec('chardet')

def test_requirement_idna():
    """Test that idna is found."""
    assert None is not import_util.find_spec('idna')

def test_requirement_requests():
    """Test that requests is found."""
    assert None is not import_util.find_spec('requests')

def test_requirement_urllib3():
    """Test that urllib3 is found."""
    assert None is not import_util.find_spec('urllib3')


# Test pytest loaded... with pytest? ¯\_(ツ)_/¯
def test_pytest():
    assert None is not import_util.find_spec('pytest')


# Test that the library itself loads

def test_self_responsysrest():
    """Test that responsysrest rest is found."""
    assert None is not import_util.find_spec('responsysrest')