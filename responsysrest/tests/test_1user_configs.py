"""Test configuration."""
import responsysrest as r


def test_credentials_class():
    """Test that the class instantiates."""
    assert r.Credentials('user', 'password', 'test@')

def test_pod_exists():
    """Test if we loaded something in the pod."""
    assert r.Configuration().pod


def test_pod_is_number_like():
    """Interact is only on one of two servers pods."""
    assert r.Configuration().pod in ['2', '5']


def test_api_folder():
    """The API folder should be a non-zero length string."""
    assert isinstance(r.Configuration().api_folder, str)
    assert 0 < len(r.Configuration().api_folder)


def test_api_list():
    """The API list should be a non-zero length string."""
    assert isinstance(r.Configuration().api_list, str)
    assert 0 < len(r.Configuration().api_list)


def test_profile_extension_table_alias():
    """The profile extension table alias should be a non-zero length string."""
    assert isinstance(r.Configuration().profile_extension_table_alias, str)
    assert 0 < len(r.Configuration().profile_extension_table_alias)


def test_supplemental_table_alias():
    """The supplemental table alias should be a non-zero length string."""
    assert isinstance(r.Configuration().supplemental_table_alias, str)
    assert 0 < len(r.Configuration().supplemental_table_alias)


def test_primary_key_alias():
    """The primary key alias should be a non-zero length string."""
    assert isinstance(r.Configuration().primary_key_alias, str)
    assert 0 < len(r.Configuration().primary_key_alias)


def test_riid_generator_length():
    """The RIID generator length should be a non-zero length string."""
    assert isinstance(r.Configuration().riid_generator_length, int)
    assert 0 < r.Configuration().riid_generator_length


def test_test_campaign_name_exists():
    """Test if we loaded something in the test campaign name."""
    assert r.Configuration().test_campaign_name


def test_test_content_library_folder_exists():
    """Test if we loaded something in the test content library folder."""
    assert r.Configuration().content_library_folder
