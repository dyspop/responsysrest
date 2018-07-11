"""Test configuration."""
import responsysrest as r

creds = r.credentials.auto()
config = r.configuration.auto()
client = r.Client(config, creds)


# test the credentials


def test_credentials_class():
    """Test that the class instantiates."""
    assert r.Credentials(
        user_name='user_name',
        password='password',
        email_address='test@test.test',
        certificates=None
    )


# test the configuration

def test_credentials_class():
    """Test that the class instantiates."""
    assert r.Configuration(
        pod="pod",
        api_folder="api_folder",
        api_list="api_list",
        profile_extension_table_alias="profile_extension_table_alias",
        supplemental_table_alias="supplemental_table_alias",
        primary_key_alias="primary_key_alias",
        riid_generator_length=11,
        test_campaign_name="test_campaign_name",
        content_library_folder="content_library_folder",
        api_version="api_version",
        test_content_library_folder="test_content_library_folder",
        local_content_library_folder="local_content_library_folder",
        test_local_content_library_folder="test_local_content_library_folder",
        user_cerficates=False
    )


def test_pod_exists():
    """Test if we loaded something in the pod."""
    assert config.pod


def test_pod_is_number_like():
    """Interact is only on one of two servers pods."""
    assert config.pod in ['2', '5']


def test_api_folder():
    """The API folder should be a non-zero length string."""
    assert isinstance(config.api_folder, str)
    assert 0 < len(config.api_folder)


def test_api_list():
    """The API list should be a non-zero length string."""
    assert isinstance(config.api_list, str)
    assert 0 < len(config.api_list)


def test_profile_extension_table_alias():
    """The profile extension table alias should be a non-zero length string."""
    assert isinstance(config.profile_extension_table_alias, str)
    assert 0 < len(config.profile_extension_table_alias)


def test_supplemental_table_alias():
    """The supplemental table alias should be a non-zero length string."""
    assert isinstance(config.supplemental_table_alias, str)
    assert 0 < len(config.supplemental_table_alias)


def test_primary_key_alias():
    """The primary key alias should be a non-zero length string."""
    assert isinstance(config.primary_key_alias, str)
    assert 0 < len(config.primary_key_alias)


def test_riid_generator_length():
    """The RIID generator length should be a non-zero length string."""
    assert isinstance(config.riid_generator_length, int)
    assert 0 < config.riid_generator_length


def test_test_campaign_name_exists():
    """Test if we loaded something in the test campaign name."""
    assert config.test_campaign_name


def test_test_remote_content_library_folder_exists():
    """Test if we loaded something in the test content library folder."""
    assert config.test_remote_content_library_folder


def test_test_local_content_library_exists():
    """Test if we loaded something for the test local content library."""
    assert config.test_local_content_library


def test_remote_content_library_folder_exists():
    """Test if we loaded something for the remote content library."""
    assert config.remote_content_library_folder


def test_local_content_library_folder_exists():
    """Test if we loaded something for the local content library."""
    assert config.local_content_library_folder


def test_caste_nonstr_to_str_exists():
    """Test if we loaded something for the option."""
    assert config.caste_nonstr_to_str


def test_caste_nonstr_to_str_is_bool():
    """Test that the value for caste types is set."""
    assert bool is type(config.caste_nonstr_to_str)


def test_config_in_client():
    """Not None."""
    assert None is not client.config


def test_creds_in_client():
    """Not None."""
    assert None is not client.creds


def test_config_matches_client_config():
    """The instantiations should match."""
    assert config == client.config


def test_creds_match_client_creds():
    """The instantiations should match."""
    assert creds == client.creds


