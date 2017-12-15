"""Tests for each individual function in the Client."""
import responsysrest as r


# Fixtures
fixtures = {
    'riid': '12112123105',
    'profile_list': 'API_testing',
    'profile_list_extension': 'API_testing_pet'
}
context = r.get_context()


# Test related functions.
def _heartbeat(func):
    """Instead of inspecting too many responses, we just test
    to see if there's something on the other end."""
    assert None is not func
    assert '' != func


# The tests.
def test_get_context_returns_authtoken():
    """Test if get_context returns an authToken.
    Some responses do warrant inspection."""
    _heartbeat(context['authToken'])


def test_get_context_returns_endpoint():
    """Test if get_context returns a responsys https endpoint.
    Some responses do warrant inspection."""
    _heartbeat(context['endPoint'])
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
    """Test if the API responds when we try to get a member."""
    _heartbeat(r.get_member_of_list_by_riid(
            fixtures['profile_list'], fixtures['riid']))


def test_fixture_riid_in_fixture_profile_list():
    """Test if the test riid is in the test profile list."""
    assert 'recordData' in r.get_member_of_list_by_riid(
        fixtures['profile_list'], fixtures['riid'])


def test_get_campaigns_not_zero_length():
    """Test to see if campaigns has data."""
    # TODO: what happens if there are no lists defined in Interact?
    assert len(r.get_campaigns()) > 0


def test_get_member_of_list_by_attribute_returns_response():
    """Test if the API responds when we get a member using
    the attribute feature."""
    _heartbeat(r.get_member_of_list_by_attribute(
            fixtures['profile_list'], fixtures['riid']))


def test_delete_from_profile_list_returns_response():
    """Test if the API responds when we try to delete a member
    from a list."""
    _heartbeat(
        r.delete_from_profile_list(fixtures['profile_list'], ''))


def test_get_profile_extensions():
    """Test if the API responds when we try to get the profile
    extensions associated with a list."""
    _heartbeat(
        r.get_profile_extensions(fixtures['profile_list']))


def test_create_profile_extension():
    """Test if the API responds when we try to create a profile extension."""
    _heartbeat(r.create_profile_extension(''))


def test_get_member_of_profile_extension_by_riid():
    """Test if the API responds when we try to get a member of
     a profile extension table."""
    _heartbeat(r.get_member_of_profile_extension_by_riid(
        fixtures['profile_list'],
        fixtures['profile_list_extension'],
        fixtures['riid'])
    )


def test_get_member_of_profile_extension_by_attribute():
    """Test if the API responds when we try to get a member of
    a profile extension table using the attribute feature."""
    _heartbeat(r.get_member_of_profile_extension_by_attribute(
        fixtures['profile_list'],
        fixtures['profile_list_extension'],
        fixtures['riid'])
    )
