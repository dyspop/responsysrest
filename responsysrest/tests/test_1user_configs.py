"""Test configuration."""
import responsysrest as r


def test_credentials_class():
    """Test that the class instantiates."""
    assert r.config.Credentials()


def test_pod_exists():
    """Test if we loaded something in the pod."""
    assert r.config.Interact().pod


def test_pod_is_number_like():
    """Interact is only on one of two servers pods."""
    assert r.config.Interact().pod in ['2', '5']


def test_api_folder():
    """The API folder should be a non-zero length string."""
    assert isinstance(r.config.Interact().api_folder, str)
    assert 0 < len(r.config.Interact().api_folder)


def test_api_list():
    """The API list should be a non-zero length string."""
    assert isinstance(r.config.Interact().api_list, str)
    assert 0 < len(r.config.Interact().api_list)


def test_profile_extension_table_alias():
    """The profile extension table alias should be a non-zero length string."""
    assert isinstance(r.config.Interact().profile_extension_table_alias, str)
    assert 0 < len(r.config.Interact().profile_extension_table_alias)


def test_supplemental_table_alias():
    """The supplemental table alias should be a non-zero length string."""
    assert isinstance(r.config.Interact().supplemental_table_alias, str)
    assert 0 < len(r.config.Interact().supplemental_table_alias)


def test_primary_key_alias():
    """The primary key alias should be a non-zero length string."""
    assert isinstance(r.config.Interact().primary_key_alias, str)
    assert 0 < len(r.config.Interact().primary_key_alias)


def test_riid_generator_length():
    """The RIID generator length should be a non-zero length string."""
    assert isinstance(r.config.Interact().riid_generator_length, int)
    assert 0 < r.config.Interact().riid_generator_length


def test_email_address_exists():
    """Test if we loaded something in the test email address."""
    assert r.config.Credentials().email_address


def test_test_campaign_name_exists():
    """Test if we loaded something in the test campaign name."""
    assert r.config.Interact().test_campaign_name


def test_test_content_library_folder_exists():
    """Test if we loaded something in the test content library folder."""
    assert r.config.Interact().content_library_folder
