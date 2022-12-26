import pytest
from hypothesis import Verbosity, given, settings, strategies

from canvasdl.utils import config, configchecker
from canvasdl.utils.path import Path


def test_valid_account():
    assert configchecker.is_valid_account(config.API_URL, config.API_KEY)


@settings(max_examples=1, deadline=5000)
@given(api_url=strategies.text())
def test_invalid_url(api_url):
    api_key = config.API_KEY
    assert not configchecker.is_valid_account(api_url, api_key)
    assert not configchecker.is_valid_url(api_url, api_key)


@given(api_string=strategies.text())
@settings(max_examples=1, deadline=5000)
def test_invalid_formatted_url(api_string):
    api_url = f"https://{api_string}.com"
    api_key = config.API_KEY
    assert not configchecker.is_valid_account(api_url, api_key)
    assert not configchecker.is_valid_url(api_url, api_key)


@settings(max_examples=1, deadline=5000, verbosity=Verbosity.verbose)
@given(api_key=strategies.text())
def test_invalid_key(api_key):
    url = config.API_URL
    assert not configchecker.is_valid_account(url, api_key)
    assert not configchecker.is_valid_key(url, api_key)


def test_google_calendar_credentials():
    assert configchecker.google_calendar_credentials_valid()


def test_custom_calendar_id():
    assert configchecker.google_calendar_credentials_valid(config.google_calendar_id)


@pytest.fixture()
def with_google_calendar_credentials_removed():
    creds = Path.calendar_credentials.json
    token = Path.calendar_token.byte_content

    paths = (Path.calendar_credentials, Path.calendar_token)
    for path in paths:
        path.unlink()

    yield
    Path.calendar_credentials.json = creds
    Path.calendar_token.byte_content = token


def test_invalid_google_calendar_credentials(with_google_calendar_credentials_removed):
    assert not configchecker.google_calendar_credentials_valid()
