"""Tests for each individual function in the Client."""
import responsysrest as r


# Fixtures
fixtures = {
    'riid': '12112123105',
    'profile_list': 'API_testing'
}


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


def test_fixture_profile_list_in_get_profile_lists():
    """Now that we know there are profile lists, test if
    the fixture list is in Interact."""
    profile_lists = [list['name'] for list in r.get_profile_lists()]
    assert fixtures['profile_list'] in profile_lists


# def test_manage_profile_lists_returns_response():
#     assert return

def test_get_member_of_list_by_riid_returns_response():
    """Test if the API responds."""
    assert None is not r.get_member_of_list_by_riid(
        fixtures['profile_list'], fixtures['riid']
    )
    assert '' != r.get_member_of_list_by_riid(
        fixtures['profile_list'], fixtures['riid']
    )


def test_fixture_riid_in_fixture_profile_list():
    assert 'recordData' in r.get_member_of_list_by_riid(
        fixtures['profile_list'], fixtures['riid']
    )


def test_get_campaigns_not_zero_length():
    """Test to see if campaigns has data."""
    # TODO: what happens if there are no lists defined in Interact?
    assert len(r.get_campaigns()) > 0


def test_get_member_of_list_by_attribute_returns_response():
    """Test if the API responds."""
    assert None is not r.get_member_of_list_by_attribute(
        fixtures['profile_list'], fixtures['riid']
    )
    assert '' != r.get_member_of_list_by_attribute(
        fixtures['profile_list'], fixtures['riid']
    )


def test_delete_from_profile_list_returns_response():
    """Test if the API responds."""
    assert None is not r.delete_from_profile_list(
        fixtures['profile_list'], ''
    )
    assert '' != r.delete_from_profile_list(
        fixtures['profile_list'], ''
    )
