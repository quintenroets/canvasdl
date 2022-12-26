import cli
from rich.prompt import Prompt

from . import configchecker
from .path import Path

DEFAULT_API_URL = "https://courseworks2.columbia.edu"


def make_config():
    Path.config_temp.yaml = {}
    # use rclone config maker
    # store api key in plaintext file and encrypt it
    # give warning that other user should also encrypt it

    ask_value(
        "API_URL",
        "Canvas url of your school",
        DEFAULT_API_URL,
        lambda url: configchecker.is_valid_url(url, ""),
    )

    config = Path.config_temp.yaml
    ask_value(
        "API_KEY",
        "Your Canvas API key",
        None,
        lambda key: configchecker.is_valid_key(config["API_URL"], key),
    )


def ask_value(name, message, default=None, check_function=None):
    base_message = message
    message_changed = False

    while name not in Path.config_temp.yaml:
        prompt = Prompt()
        response = prompt.ask(message, default=default)
        valid_response = check_function is None
        if not valid_response:
            with cli.status(f"Checking {base_message}"):
                valid_response = check_function(response)

        if valid_response:
            Path.config_temp.yaml |= {name: response}
        elif not message_changed:
            message = f"Error: please provide valid value for {message}"
            message_changed = True
