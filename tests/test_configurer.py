from hypothesis import Verbosity, given, settings, strategies

from canvasdl.utils import config, configchecker


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
