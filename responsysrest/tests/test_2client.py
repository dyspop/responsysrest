"""Tests for each individual function in the Client."""
import responsysrest as r
import random

creds = r.credentials.auto()
config = r.Configuration()

# Fixtures
# Set the riid once before execution outside the fixtures dict
fixture_riid = ''.join(
    [
        str(n) for n in
        [random.randint(0, 9) for x in range(0, config.riid_generator_length)]
    ]
)
fixtures = {
    'folder': config.api_folder,
    'riid': fixture_riid,
    'profile_list': config.api_list,
    'profile_list_extension': f'{config.api_list}{config.profile_extension_table_alias}',
    'primary_key': f'{config.api_list}{config.primary_key_alias}',
    'email_address': creds.email_address,
    'campaign_name': config.test_campaign_name
}
context = r.get_context(creds.user_name, creds.password, config.login_url)


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
    assert len(r.get_profile_lists(context)) > 0


def test_fixture_profile_list_in_get_profile_lists():
    """Test if the fixture list is in Interact."""
    profile_lists = [list['name'] for list in r.get_profile_lists(context)]
    assert fixtures['profile_list'] in profile_lists


def test_get_campaigns_not_zero_length():
    """Test to see if campaigns has data."""
    # TODO: what happens if there are no campaigns defined in Interact?
    assert len(r.get_campaigns(context)) > 0


# def test_manage_profile_lists_returns_response():
#     assert return


def test_get_member_of_list_by_riid_returns_response():
    """Test if the API responds when we try to get a member."""
    assert _heartbeat(r.get_member_of_list_by_riid(
        fixtures['profile_list'], fixtures['riid'], context))


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
        fixtures['profile_list'], fixtures['riid'], context))


def test_delete_from_profile_list_returns_response():
    """Test if the API responds.

    When we try to delete a member from a list.
    """
    assert _heartbeat(
        r.delete_from_profile_list(fixtures['profile_list'], '', context))


def test_get_profile_extensions():
    """Test if the API responds.

    When we try to get the profile extensions associated with a list.
    """
    assert _heartbeat(
        r.get_profile_extensions(fixtures['profile_list'], context))


def test_create_profile_extension():
    """Test if the API responds.

    When we try to create a profile extension.
    Heartbeat is expected whether create a new one or
    try to create one that exists.
    """
    assert _heartbeat(
        r.create_profile_extension(fixtures['profile_list_extension'], context))


def test_get_member_of_profile_extension_by_riid():
    """Test if the API responds.

    When we try to get a member of a profile extension table.
    """
    assert _heartbeat(r.get_member_of_profile_extension_by_riid(
        fixtures['profile_list'],
        fixtures['profile_list_extension'],
        fixtures['riid'],
        context)
    )


def test_get_member_of_profile_extension_by_attribute():
    """Test if the API responds.

    When we try to get a member of a profile extension table by attribute.
    """
    assert _heartbeat(r.get_member_of_profile_extension_by_attribute(
        fixtures['profile_list'],
        fixtures['profile_list_extension'],
        fixtures['riid'],
        context)
    )


def test_delete_member_of_profile_extension_by_riid():
    """Test if the API responds.

    When we try to delete a member of a profile extension table by riid.
    We don't use fixtures so that we don't delete anything!
    """
    assert _heartbeat(
        r.delete_member_of_profile_extension_by_riid('', '', '', context))


def test_create_supplemental_table():
    """Test if the API responds.

    When we try to create a supplemental table.
    We don't use fixtures so that we don't delete anything!
    """
    assert _heartbeat(r.create_supplemental_table(
        fixtures['profile_list'],
        context,
        fixtures['folder'],
        [fixtures['primary_key']])
    )


def test_get_push_campaigns_returns_response():
    """Test if the API responds.

    When we try to list all push campaigns.
    """
    assert _heartbeat(r.get_push_campaigns(context))


def test_send_email_message_returns_response():
    """Test if the API responds.

    When we try to send a message, good or bad.
    """
    assert _heartbeat(r.send_email_message(
        fixtures['email_address'],
        fixtures['folder'],
        fixtures['campaign_name'],
        context)
    )


def test_create_folder_returns_response():
    """Test if the API responds.

    When we try to list all push campaigns.
    """
    assert _heartbeat(r.create_folder(
        context,
        config.content_library_folder))


def test_delete_folder_returns_response():
    """Test if the API responds.

    When we try to delete a content library folder.
    """
    assert _heartbeat(r.delete_folder(
        config.content_library_folder))
