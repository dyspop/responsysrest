"""Tests for each individual function in the Client."""
import responsysrest as r

context = r.get_context()


def test_get_context_returns_authtoken():
    """Test if get_context returns an authToken."""
    assert None is not context['authToken']
    assert '' != context['authToken']


def test_get_context_returns_endpoint():
    """Test if get_context returns a responsys https endpoint."""
    assert None is not context['endPoint']
    assert '' != context['endPoint']
    before, https, after = context['endPoint'].rpartition('https://')
    assert '' == before
    assert 'https://' == https
    assert 'responsys.' in after


def test_get_profile_lists_not_zero_length():
    """Test to see if profile lists has data."""
    # TODO: what happens if there are no lists defined in Interact?
    assert len(r.get_profile_lists()) > 0


def test_get_campaigns_not_zero_length():
    """Test to see if campaigns has data."""
    # TODO: what happens if there are no lists defined in Interact?
    assert len(r.get_campaigns()) > 0
