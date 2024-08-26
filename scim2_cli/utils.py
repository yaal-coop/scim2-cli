import json
from enum import Enum
from typing import Dict
from typing import List

import click
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

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


def split_headers(headers: List[str]) -> Dict[str, str]:
    """Make a dict from header strings.

    ['Authorization: Bearer token'] → '{"Authorization": "Bearer
    token"}'
    """

    return {
        header[: header.index(":")].strip(): header[header.index(":") + 1 :].strip()
        for header in headers
    }


RSTCommand: click.Group = make_rst_to_ansi_formatter(DOC_URL, group=True)


class ModelCommand(RSTCommand):
    """CLI commands that takes a model subcommand."""

    def __init__(self, *args, factory, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = factory

    def list_commands(self, ctx):
        ctx.ensure_object(dict)
        base = super().list_commands(ctx)
        lazy = sorted(ctx.obj.get("resource_types", {}).keys())
        return base + lazy

    def get_command(self, ctx, cmd_name):
        model = ctx.obj["resource_types"].get(cmd_name)
        return self.factory(model)


def is_field_acceptable(context, model, field_name) -> bool:
    """Indicate whether a field is acceptable as part of a SCIM payload for a
    given context."""

    from scim2_models import Context
    from scim2_models import Mutability

    mutability = model.get_field_annotation(field_name, Mutability)

    if (
        context
        in (Context.RESOURCE_CREATION_REQUEST, Context.RESOURCE_REPLACEMENT_REQUEST)
        and mutability == Mutability.read_only
    ):
        return False

    if (
        context in (Context.RESOURCE_QUERY_REQUEST, Context.SEARCH_REQUEST)
        and mutability == Mutability.write_only
    ):
        return False

    if (
        context == Context.RESOURCE_REPLACEMENT_REQUEST
        and mutability == Mutability.immutable
    ):
        return False

    return True


def unacceptable_fields(context, model):
    return [
        field_name
        for field_name in model.model_fields
        if not is_field_acceptable(context, model, field_name)
    ]
