"""Tests for each individual function in the Client."""
import responsysrest as r
import random
import string
import requests
import pytest

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
    'api_username': creds.user_name,
    'campaign_name': config.test_campaign_name,
    'document': './responsysrest/tests/document.htm',
    'content_library_folder': '___api-generated-test'
}


def _random_string(N=256):
    # Generate a random string of N or 256 chars long
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))


# Test-related functions.
def _heartbeat(func):
    """Test if the API responds.

    Instead of inspecting too many responses, we just test
    to see if there's something on the other end.
    """
    return (None is not func and '' != func)


def _bad_request(func):
    return (
        isinstance(func, requests.models.Response),
        func.status_code == 404)


""" The tests for logging in and managing the client context."""


def test_login_returns_response():
    """Test login."""
    assert client._login(
        creds.user_name, creds.password, config.login_url)

@pytest.mark.xfail
def test_login_with_username_and_certificates():
    """Test login with certificates."""
    assert client._login_with_username_and_certificates(
        creds.user_name, creds.certificates)


def test_get_context():
    assert _heartbeat(client._get_context())


def test_get_context_returns_authtoken():
    """Test if get_context returns an authToken.

    Some responses do warrant inspection.
    """
    assert _heartbeat(client._get_context()['authToken'])


def test_get_context_returns_endpoint():
    """Test if get_context returns a responsys https endpoint."""
    assert _heartbeat(client._get_context()['endPoint'])


def test_get_context_endpoint_is_https_and_responsys():
    """Some responses do warrant inspection."""
    a, m, z = client._get_context()['endPoint'].rpartition('https://')
    assert '' == a
    assert 'https://' == m
    assert 'responsys.' in z


@pytest.mark.xfail
def test_refresh_token():
    """Test refreshing the token."""
    assert client._refresh_token(None)


"""The tests for the internal CRUD methods bound to context."""


def test_get():
    """Test to see if the server responds when we try to get a bad request."""
    assert _bad_request(client._get(None))


def test_post():
    """Test to see if the server responds when we try to post a bad request."""
    assert _bad_request(client._post(None, None))


def test_delete():
    """Test to see if the server responds when we try to delete nothing."""
    assert _bad_request(client._delete(None))


"""Tests for API functions."""


def test_get_profile_lists_not_zero_length():
    """Test to see if profile lists has data."""
    # TODO: what happens if there are no lists defined in Interact?
    assert len(client.get_profile_lists()) > 0


@pytest.mark.xfail
def test_update_profile_list():
    """Test updating a profile list."""
    assert client.update_profile_list(None)


def test_fixture_profile_list_in_get_profile_lists():
    """Test if the fixture list is in Interact."""
    profile_lists = [list['name'] for list in client.get_profile_lists()]
    error_message = 'You must manually create a {l} test profile list in Interact UI.'.format(l=config.api_list)
    assert fixtures['profile_list'] in profile_lists, error_message


def test_get_campaigns_not_zero_length():
    """Test to see if campaigns has data."""
    # TODO: what happens if there are no campaigns defined in Interact?
    assert len(client.get_campaigns()) > 0


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

@pytest.mark.xfail
def test_create_profile_extension():
    """Test if the API responds.

    When we try to create a profile extension.
    Heartbeat is expected whether create a new one or
    try to create one that exists.
    """
    assert _heartbeat(
        client.create_profile_extension(fixtures['profile_list_extension']))

@pytest.mark.xfail
def test_update_profile_extension():
    """Test updating a profile list."""
    assert client.update_profile_extension(None)


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


@pytest.mark.xfail
def test_update_supplemental_table():
    """Test updating a supplemental table."""
    assert client.update_supplemental_table(None, None, None)


def test_get_push_campaigns_returns_response():
    """Test if the API responds.

    When we try to list all push campaigns.
    """
    assert _heartbeat(client.get_push_campaigns())


@pytest.mark.xfail
def test_get_record_from_supplemental_table():
    """Test getting a record from a supplemental table."""
    assert client.get_record_from_supplemental_table(None, None, None)


@pytest.mark.xfail
def test_delete_record_from_supplemental_table():
    """Test deleting a record from a supplemental table."""
    assert client.delete_record_from_supplemental_table(None, None, None)


@pytest.mark.xfail
def test_update_list_and_send_email_message():
    """Test update list and send email."""
    assert client.update_list_and_send_email_message(None, None)


@pytest.mark.xfail
def test_update_list_and_send_email_message_with_attachments():
    """Test update list and send email with attachment."""
    assert client.update_list_and_send_email_message_with_attachments(
        None, None, None)


def test_send_email_message_returns_response():
    """Test if the API responds.

    When we try to send a message, most likely to garbage entries.
    """
    assert _heartbeat(client.send_email_message(
        _random_string(), _random_string(), _random_string()
    ))


# Valid test but now we're spamming outselves
def test_send_email_message_returns_response_for_send_to_one_recipient():
    assert _heartbeat(client.send_email_message(
        fixtures['email_address'],
        fixtures['folder'],
        fixtures['campaign_name']))


# Valid test but now we're spamming outselves
def test_send_email_message_returns_success_for_send_to_one_recipient():
    resp = client.send_email_message(
        fixtures['email_address'],
        fixtures['folder'],
        fixtures['campaign_name'])
    assert list is type(resp)
    assert 1 is len(resp) 
    assert dict is type(resp[0])
    assert 'errorMessage' in resp[0].keys()
    assert 'success' in resp[0].keys()
    assert 'recipientId' in resp[0].keys()
    assert None is resp[0]['errorMessage']
    assert True is resp[0]['success']
    assert None is not resp[0]['recipientId']
    assert False is not resp[0]['recipientId']


@pytest.mark.xfail
def test_update_list_and_send_sms():
    """Test update list and send SMS."""
    assert client.update_list_and_send_sms(None, None)


@pytest.mark.xfail
def test_send_push_message():
    """Test sending a push message."""
    assert client.send_push_message(None, None)


@pytest.mark.xfail
def test_trigger_custom_event():
    """Test triggering a custom event."""
    assert client.trigger_custom_event(None, None)


@pytest.mark.xfail
def test_schedule_campaign():
    """Test scheduling a campaign."""
    assert client.schedule_campaign(None, None, None, None)


@pytest.mark.xfail
def test_get_schedules_for_campaign():
    """Test getting the schedules related to a campaign."""
    assert client.get_schedules_for_campaign()


@pytest.mark.xfail
def test_get_campaign_schedule():
    """Test returning a campaign schedule."""
    assert client.get_campaign_schedule(None, None)


@pytest.mark.xfail
def test_update_campaign_schedule():
    """Test updating an existing schedule."""
    assert client.update_campaign_schedule(None, None, None, None)


@pytest.mark.xfail
def test_unschedule_campaign():
    """Test unscheduling a campaign."""
    assert client.unschedule_campaign(None, None)


def test_create_folder_returns_response():
    """Test if the API responds.

    When we try to list all push campaigns.
    """
    assert _heartbeat(client.create_folder(fixtures['content_library_folder']))


@pytest.mark.xfail
def test_list_folder():
    """Test listing a content library folder."""
    assert client.list_folder(None)


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
    assert _heartbeat(client.get_document(fixtures['document']))


def test_get_document_returns_document_at_config_path():
    """Test if the API's response document is at the config path."""
    assert client.get_document(fixtures['document'])[
        'documentPath'].startswith(
            '/contentlibrary/{f}/'.format(
                f=fixtures['content_library_folder']
            )
        )


def test_update_document_returns_response():
    """Test if the API responds.

    When we try to create a content library document.
    """
    assert _heartbeat(client.update_document(fixtures['document']))


def test_delete_document_returns_response():
    """Test if the API responds.

    When we try to create a content library document.
    """
    assert _heartbeat(client.delete_document(fixtures['document']))


def test_update_profile_list_returns_response():
    """Test if the API responds."""
    assert _heartbeat(client.update_profile_list(
        fixtures['profile_list'], ['RIID_'], fixtures['riid']))


@pytest.mark.xfail
def test_create_media_file():
    """Test creating a media file on Responsys Interact."""
    assert client.create_media_file(None)


@pytest.mark.xfail
def test_get_media_file():
    """Test getting a media file from Responsys Interact."""
    assert client.get_media_file(None)


@pytest.mark.xfail
def test_update_media_file():
    """Test updating an existing file on Responsys Interact."""
    assert client.update_media_file(None, None)


@pytest.mark.xfail
def test_delete_media_file():
    """Test deleting a media file on Responsys Interact."""
    assert client.delete_media_file(None)


@pytest.mark.xfail
def test_copy_media_file():
    """Test generating a copy of a file on Responsys Interact."""
    assert client.copy_media_file(None, None)


@pytest.mark.xfail
def test_set_images_in_document():
    """Test setting an image in a content library document."""
    assert client.set_images_in_document(None, None, None, None)


@pytest.mark.xfail
def test_get_images_in_document():
    """Test getting images from a content library document."""
    assert client.get_images_in_document(None)
