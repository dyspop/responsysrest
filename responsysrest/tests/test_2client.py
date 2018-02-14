"""Tests for each individual function in the Client."""
import responsysrest as r
import random

creds = r.config.Credentials()
interact = r.config.Interact()

# Fixtures
# Set the riid once before execution outside the fixtures dict
fixture_riid = ''.join(
    [
        str(n) for n in
        [random.randint(0, 9) for x in range(0, r.config.Interact().riid_generator_length)]
    ]
)
fixtures = {
    'folder': r.config.Interact().api_folder,
    'riid': fixture_riid,
    'profile_list': r.config.Interact().api_list,
    'profile_list_extension': f'{r.config.Interact().api_list}{r.config.Interact().profile_extension_table_alias}',
    'primary_key': f'{r.config.Interact().api_list}{r.config.Interact().primary_key_alias}',
    'email_address': r.config.Credentials().email_address,
    'campaign_name': r.config.Interact().test_campaign_name
}
context = r.get_context(creds.user_name, creds.password, r.config.Interact().login_url)


# Test related functions.
def _heartbeat(func):
    """Test if the API responds.

    Instead of inspecting too many responses, we just test
    to see if there's something on the other end.
    """
    return (None is not func and '' != func)


# The tests.
def test_get_context_returns_authtoken():
    """Test if get_context returns an authToken.

    Some responses do warrant inspection.
    """
    assert _heartbeat(context['authToken'])


def test_get_context_returns_endpoint():
    """Test if get_context returns a responsys https endpoint."""
    assert _heartbeat(context['endPoint'])


def test_get_context_endpoint_is_https_and_responsys():
    """Some responses do warrant inspection."""
    before, https, after = context['endPoint'].rpartition('https://')
    assert '' == before
    assert 'https://' == https
    assert 'responsys.' in after


def test_get_profile_lists_not_zero_length():
    """Test to see if profile lists has data."""
    # TODO: what happens if there are no lists defined in Interact?
    assert len(r.get_profile_lists()) > 0


def test_fixture_profile_list_in_get_profile_lists():
    """Test if the fixture list is in Interact."""
    profile_lists = [list['name'] for list in r.get_profile_lists()]
    assert fixtures['profile_list'] in profile_lists


def test_get_campaigns_not_zero_length():
    """Test to see if campaigns has data."""
    # TODO: what happens if there are no campaigns defined in Interact?
    assert len(r.get_campaigns()) > 0


# def test_manage_profile_lists_returns_response():
#     assert return


def test_get_member_of_list_by_riid_returns_response():
    """Test if the API responds when we try to get a member."""
    assert _heartbeat(r.get_member_of_list_by_riid(
        fixtures['profile_list'], fixtures['riid']))


# def test_fixture_riid_in_fixture_profile_list():
#     """Test if the test riid is in the test profile list."""
#     # Add the record to the test list
#     print(fixtures['riid'])
#     r.manage_profile_list(
        # fixtures['profile_list'], records=[fixtures['riid']])
#     assert 'recordData' in r.get_member_of_list_by_riid(
#         fixtures['profile_list'], fixtures['riid'])


def test_get_member_of_list_by_attribute_returns_response():
    """Test if the API responds.

    When we get a member using the attribute feature.
    """
    assert _heartbeat(r.get_member_of_list_by_attribute(
        fixtures['profile_list'], fixtures['riid']))


def test_delete_from_profile_list_returns_response():
    """Test if the API responds.

    When we try to delete a member from a list.
    """
    assert _heartbeat(
        r.delete_from_profile_list(fixtures['profile_list'], ''))


def test_get_profile_extensions():
    """Test if the API responds.

    When we try to get the profile extensions associated with a list.
    """
    assert _heartbeat(
        r.get_profile_extensions(fixtures['profile_list']))


def test_create_profile_extension():
    """Test if the API responds.

    When we try to create a profile extension.
    Heartbeat is expected whether create a new one or
    try to create one that exists.
    """
    assert _heartbeat(
        r.create_profile_extension(fixtures['profile_list_extension']))


def test_get_member_of_profile_extension_by_riid():
    """Test if the API responds.

    When we try to get a member of a profile extension table.
    """
    assert _heartbeat(r.get_member_of_profile_extension_by_riid(
        fixtures['profile_list'],
        fixtures['profile_list_extension'],
        fixtures['riid'])
    )


def test_get_member_of_profile_extension_by_attribute():
    """Test if the API responds.

    When we try to get a member of a profile extension table by attribute.
    """
    assert _heartbeat(r.get_member_of_profile_extension_by_attribute(
        fixtures['profile_list'],
        fixtures['profile_list_extension'],
        fixtures['riid'])
    )


def test_delete_member_of_profile_extension_by_riid():
    """Test if the API responds.

    When we try to delete a member of a profile extension table by riid.
    We don't use fixtures so that we don't delete anything!
    """
    assert _heartbeat(r.delete_member_of_profile_extension_by_riid('', '', ''))


def test_create_supplemental_table():
    """Test if the API responds.

    When we try to create a supplemental table.
    We don't use fixtures so that we don't delete anything!
    """
    assert _heartbeat(r.create_supplemental_table(
        fixtures['profile_list'],
        fixtures['folder'],
        [fixtures['primary_key']])
    )


def test_get_push_campaigns_returns_response():
    """Test if the API responds.

    When we try to list all push campaigns.
    """
    assert _heartbeat(r.get_push_campaigns())


def test_send_email_message_returns_response():
    """Test if the API responds.

    When we try to send a message, good or bad.
    """
    assert _heartbeat(r.send_email_message(
        fixtures['email_address'],
        fixtures['folder'],
        fixtures['campaign_name'])
    )


def test_create_folder_returns_response():
    """Test if the API responds.

    When we try to list all push campaigns.
    """
    assert _heartbeat(r.create_folder(
        config.test_content_library_folder))


def test_delete_folder_returns_response():
    """Test if the API responds.

    When we try to delete a content library folder.
    """
    assert _heartbeat(r.delete_folder(
        config.test_content_library_folder))
