"""Tests for each individual function in the Extra Features set."""
import responsysrest as r

creds = r.credentials.auto()
config = r.configuration.auto()
client = r.Client(config, creds)


# Test related functions.
def _heartbeat(func):
    """Test if the API responds.

    Instead of inspecting too many responses, we just test
    to see if there's something on the other end.
    """
    return (None is not func and '' != func)


def test_get_lists_for_record_returns_response():
    """Test if the API responds.

    When we try to get the lists associated with a given RIID.
    """
    assert _heartbeat(client.get_lists_for_record('0'))
