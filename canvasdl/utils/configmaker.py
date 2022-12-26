from __future__ import annotations

import typing

import cli
from rich.prompt import Confirm, Prompt

from . import configchecker
from .path import Path

if typing.TYPE_CHECKING:
    from canvasdl.asset_types import Course  # noqa: autoimport


DEFAULT_API_URL = "https://courseworks2.columbia.edu"


def make_config():
    Path.config.yaml = {}
    # store api key in plaintext file and encrypt it
    # give warning that other user should also encrypt it

    ask_value(
        "API_URL",
        "Canvas url of your school",
        DEFAULT_API_URL,
        lambda url: configchecker.is_valid_url(url, ""),
    )

    config = Path.config.yaml
    ask_value(
        "API_KEY",
        "Your Canvas API key",
        None,
        lambda key: configchecker.is_valid_key(config["API_URL"], key),
    )

    question = (
        "Do you want to synchronize all important deadlines with your google calendar?"
    )
    sync_calendar = Confirm().ask(question, default=True)

    if sync_calendar:
        dummy_name = "CREDS"
        if not configchecker.google_calendar_credentials_valid():
            ask_value(
                dummy_name,
                "Please obtain a google calendar credentials file (instructions in"
                f" Readme) and save it to {Path.calendar_credentials} (press enter when"
                " done)",
                None,
                lambda response: configchecker.google_calendar_credentials_valid(),
            )
            Path.config.yaml = Path.config.yaml.pop(dummy_name)

        config = Path.config.yaml
        if "google_calendar_id" not in config:
            question = (
                "Do you want to use a custom calendar id? (only relevant if your"
                " account has multiple calendars)"
            )
            if Confirm().ask(question, default=False):
                ask_value(
                    "google_calendar_id",
                    "Id of your google calendar",
                    None,
                    lambda id: configchecker.google_calendar_credentials_valid(id),
                )


def ask_value(name, message, default=None, check_function=None):
    base_message = message
    message_changed = False

    while name not in Path.config.yaml:
        prompt = Prompt()
        response = prompt.ask(message, default=default)
        valid_response = check_function is None
        if not valid_response:
            with cli.status(f"Checking {base_message}"):
                valid_response = check_function(response)

        if valid_response:
            Path.config.yaml |= {name: response}
        elif not message_changed:
            message = f"Error: please provide valid value for {message}"
            message_changed = True
