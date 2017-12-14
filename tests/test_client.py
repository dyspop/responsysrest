"""Tests for each individual function in the Client."""
import responsysrest as r

context = r.get_context()


def test_does_get_context_get_auth():
    """Test if get_context returns an authToken."""
    assert None is not context['authToken']
    assert '' != context['authToken']


def test_does_get_context_get_endpoint():
    """Test if get_context return an https endpoint."""
    assert None is not context['endPoint']
    assert '' != context['endPoint']
    before, https, after = context['endPoint'].rpartition('https://')
    assert '' == before
    assert 'https://' == https
    assert 'responsys.' in after


def test_profile_lists():
    """Test to see if profile lists has data."""
    # TODO: what happens if there are no lists defined in Interact?
    assert len(r.profile_lists()) > 0
