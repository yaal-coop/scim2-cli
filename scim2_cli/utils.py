import json
from enum import Enum

DOC_URL = "https://scim2-cli.readthedocs.io/"
INDENTATION_SIZE = 4


class Color(str, Enum):
    black = "black"
    red = "red"
    green = "green"
    yellow = "yellow"
    blue = "blue"
    magenta = "magenta"
    cyan = "cyan"
    white = "white"
    bright_black = "bright_black"
    bright_red = "bright_red"
    bright_green = "bright_green"
    bright_yellow = "bright_yellow"
    bright_blue = "bright_blue"
    bright_magenta = "bright_magenta"
    bright_cyan = "bright_cyan"
    bright_white = "bright_white"


def formatted_payload(obj, indent):
    indent = INDENTATION_SIZE if indent else False
    return json.dumps(obj, indent=indent)


def split_headers(headers):
    return {
        header[: header.index(":")].strip(): header[header.index(":") + 1 :].strip()
        for header in headers
    }
