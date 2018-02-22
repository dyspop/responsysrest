"""Tests for each individual function in the Client."""
import responsysrest as r
import random

creds = r.credentials.auto()
config = r.configuration.auto()
client = r.Client(config, creds)

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
    'campaign_name': config.test_campaign_name,
    'document': './responsysrest/tests/document.html',
    'content_library_folder': '___api-generated-test'
}
context = client._get_context()


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
    assert len(client.get_profile_lists()) > 0


def test_fixture_profile_list_in_get_profile_lists():
    """Test if the fixture list is in Interact."""
    profile_lists = [list['name'] for list in client.get_profile_lists()]
    assert fixtures['profile_list'] in profile_lists


def test_get_campaigns_not_zero_length():
    """Test to see if campaigns has data."""
    # TODO: what happens if there are no campaigns defined in Interact?
    assert len(client.get_campaigns()) > 0


# def test_manage_profile_lists_returns_response():
#     assert return


def test_get_member_of_list_by_riid_returns_response():
    """Test if the API responds when we try to get a membeclient."""
    assert _heartbeat(client.get_member_of_list_by_riid(
        fixtures['profile_list'], fixtures['riid']))


# def test_fixture_riid_in_fixture_profile_list():
#     """Test if the test riid is in the test profile list."""
#     # Add the record to the test list
#     print(fixtures['riid'])
#     client.manage_profile_list(
        # fixtures['profile_list'], records=[fixtures['riid']])
#     assert 'recordData' in client.get_member_of_list_by_riid(
#         fixtures['profile_list'], fixtures['riid'])


def test_get_member_of_list_by_attribute_returns_response():
    """Test if the API responds.

    When we get a member using the attribute feature.
    """
    assert _heartbeat(client.get_member_of_list_by_attribute(
        fixtures['profile_list'], fixtures['riid']))


def test_delete_from_profile_list_returns_response():
    """Test if the API responds.

    When we try to delete a member from a list.
    """
    assert _heartbeat(
        client.delete_from_profile_list(fixtures['profile_list'], ''))


def test_get_profile_extensions_for_list():
    """Test if the API responds.

    When we try to get the profile extensions associated with a list.
    """
    assert _heartbeat(
        client.get_profile_extensions_for_list(fixtures['profile_list']))


def test_create_profile_extension():
    """Test if the API responds.

    When we try to create a profile extension.
    Heartbeat is expected whether create a new one or
    try to create one that exists.
    """
    assert _heartbeat(
        client.create_profile_extension(fixtures['profile_list_extension']))


def test_get_member_of_profile_extension_by_riid():
    """Test if the API responds.

    When we try to get a member of a profile extension table.
    """
    assert _heartbeat(client.get_member_of_profile_extension_by_riid(
        fixtures['profile_list'],
        fixtures['profile_list_extension'],
        fixtures['riid']))


def test_get_member_of_profile_extension_by_attribute():
    """Test if the API responds.

    When we try to get a member of a profile extension table by attribute.
    """
    assert _heartbeat(client.get_member_of_profile_extension_by_attribute(
        fixtures['profile_list'],
        fixtures['profile_list_extension'],
        fixtures['riid']))


def test_delete_member_of_profile_extension_by_riid():
    """Test if the API responds.

    When we try to delete a member of a profile extension table by riid.
    We don't use fixtures so that we don't delete anything!
    """
    assert _heartbeat(
        client.delete_member_of_profile_extension_by_riid('', '', ''))


def test_create_supplemental_table():
    """Test if the API responds.

    When we try to create a supplemental table.
    """
    assert _heartbeat(client.create_supplemental_table(
        fixtures['profile_list'],
        fixtures['folder'],
        [fixtures['primary_key']]))


def test_get_push_campaigns_returns_response():
    """Test if the API responds.

    When we try to list all push campaigns.
    """
    assert _heartbeat(client.get_push_campaigns())


def test_send_email_message_returns_response():
    """Test if the API responds.

    When we try to send a message, good or bad.
    """
    assert _heartbeat(client.send_email_message(
        fixtures['email_address'],
        fixtures['folder'],
        fixtures['campaign_name']))


def test_create_folder_returns_response():
    """Test if the API responds.

    When we try to list all push campaigns.
    """
    assert _heartbeat(client.create_folder(fixtures['content_library_folder']))


def test_delete_folder_returns_response():
    """Test if the API responds.

    When we try to delete a content library folder.
    """
    assert _heartbeat(client.delete_folder(fixtures['content_library_folder']))


def test_create_document_returns_response():
    """Test if the API responds.

    When we try to create a content library document.
    """
    assert _heartbeat(client.create_document(fixtures['document']))


def test_get_document_returns_response():
    """Test if the API responds.

    When we try to create a content library document.
    """
    assert _heartbeat(client.get_document(''))

