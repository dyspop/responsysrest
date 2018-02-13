"""Test configuration."""
from .responsysrest import responsysrest as r

def test_configuration_class():
    """Test that the class instantiates."""
    assert r.Configuration()

# """Test user configuration."""
# import config


# def test_import_config():
#     """Test everything the config, the user may not have added them."""
#     assert None is not config
#     assert '' != config


# def test_pod_exists():
#     """Test if we loaded something in the pod."""
#     assert config.pod


# def test_pod_is_number_like():
#     """Interact is only on one of two servers pods."""
#     assert config.pod in ['2', '5']


# def test_api_folder():
#     """The API folder should be a non-zero length string."""
#     assert isinstance(config.api_folder, str)
#     assert 0 < len(config.api_folder)


# def test_api_list():
#     """The API list should be a non-zero length string."""
#     assert isinstance(config.api_list, str)
#     assert 0 < len(config.api_list)


# def test_profile_extension_table_alias():
#     """The profile extension table alias should be a non-zero length string."""
#     assert isinstance(config.profile_extension_table_alias, str)
#     assert 0 < len(config.profile_extension_table_alias)


# def test_supplemental_table_alias():
#     """The supplemental table alias should be a non-zero length string."""
#     assert isinstance(config.supplemental_table_alias, str)
#     assert 0 < len(config.supplemental_table_alias)


# def test_primary_key_alias():
#     """The primary key alias should be a non-zero length string."""
#     assert isinstance(config.primary_key_alias, str)
#     assert 0 < len(config.primary_key_alias)


# def test_riid_generator_length():
#     """The RIID generator length should be a non-zero length string."""
#     assert isinstance(config.riid_generator_length, int)
#     assert 0 < config.riid_generator_length


# def test_test_email_address_exists():
#     """Test if we loaded something in the test email address."""
#     assert config.test_email_address


# def test_test_campaign_name_exists():
#     """Test if we loaded something in the test campaign name."""
#     assert config.test_campaign_name


# def test_test_content_library_folder_exists():
#     """Test if we loaded something in the test content library folder."""
#     assert config.test_content_library_folder
