import requests
from canvasapi import Canvas, exceptions


def is_valid_account(url, key):
    return is_valid_url(url, key) and is_valid_key(url, key)


def is_valid_url(url, key):
    invalid_exceptions = (
        requests.exceptions.MissingSchema,
        requests.exceptions.JSONDecodeError,
    )
    ignored_exceptions = (
        exceptions.InvalidAccessToken,
        StopIteration,
        exceptions.ResourceDoesNotExist,
    )
    is_valid = usage_works(url, key, invalid_exceptions, ignored_exceptions)
    return is_valid


def is_valid_key(url, key):
    invalid_exceptions = (
        exceptions.InvalidAccessToken,
        exceptions.ResourceDoesNotExist,
    )
    ignored_exceptions = (StopIteration,)
    return usage_works(url, key, invalid_exceptions, ignored_exceptions)


def usage_works(url, key, exceptions, ignored_exceptions):
    works = is_valid_url_scheme(url)
    if works:
        client = Canvas(url, key)
        accounts = client.get_accounts()
        try:
            next(iter(accounts))
        except exceptions:
            works = False
        except ignored_exceptions:
            pass
    return works


def is_valid_url_scheme(url):
    is_valid = True
    try:
        api_url = f"{url}/api/v1"
        requests.head(api_url)
    except ValueError:
        is_valid = False
    return is_valid
