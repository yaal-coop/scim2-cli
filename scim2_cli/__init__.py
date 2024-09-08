import json

import click
from httpx import Client
from scim2_client import SCIMClient
from scim2_models import Group
from scim2_models import User
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

from scim2_cli.create import create_cli
from scim2_cli.delete import delete_cli
from scim2_cli.query import query_cli
from scim2_cli.replace import replace_cli
from scim2_cli.search import search_cli
from scim2_cli.test import test_cli
from scim2_cli.utils import DOC_URL


@click.group(cls=make_rst_to_ansi_formatter(DOC_URL, group=True))
@click.argument("url")
@click.pass_context
def cli(ctx, url):
    """SCIM application development CLI."""

    ctx.ensure_object(dict)
    ctx.obj["URL"] = url
    client = Client(base_url=ctx.obj["URL"])
    ctx.obj["client"] = SCIMClient(client, resource_types=(User, Group))
    ctx.obj["resource_types"] = {
        resource_type.__name__.lower(): resource_type
        for resource_type in ctx.obj["client"].resource_types
    }

    if not click.get_text_stream("stdin").isatty():  # pragma: no cover
        if stdin := click.get_text_stream("stdin").read().strip():
            try:
                ctx.obj["stdin"] = json.loads(stdin)
            except json.JSONDecodeError as exc:
                message = f"Invalid JSON input.\n{exc}"
                raise click.ClickException(message) from exc


cli.add_command(create_cli)
cli.add_command(query_cli)
cli.add_command(replace_cli)
cli.add_command(delete_cli)
cli.add_command(search_cli)
cli.add_command(test_cli)

if __name__ == "__main__":  # pragma: no cover
    cli()
