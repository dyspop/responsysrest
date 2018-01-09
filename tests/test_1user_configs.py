"""Test user configuration."""
import config


def test_import_config():
    """Test everything the config, the user may not have added them."""
    for k in config:
        assert None is not config[k]
        assert '' != config[k]
