"""Test user configuration."""
import config


def test_import_config():
    """Test everything the config, the user may not have added them."""
    assert None is not config
    assert '' != config


def test_pod_exists():
    """Test if we loaded something in the pod."""
    assert config.pod


def test_pod_is_number_like():
    """Responsys Interact is only on one of two servers pods"""
    assert str(config.pod) in ['2', '5']
