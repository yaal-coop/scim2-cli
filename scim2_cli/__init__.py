import json
from typing import Any
from typing import TypeGuard

import click
from httpx import Client
from pydantic import BaseModel
from scim2_client.engines.httpx import SyncSCIMClient
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
from scim2_cli.utils import HeaderType

from .utils import split_headers


# monkeypatching pydanclick until this patch is released
# https://github.com/felix-martel/pydanclick/pull/25
def patch_pydanclick():
    def _is_pydantic_model(model: Any) -> TypeGuard[type[BaseModel]]:
        """Return True if `model` is a Pydantic `BaseModel` class."""
        try:
            return issubclass(model, BaseModel)
        except TypeError:
            return False

    import pydanclick.model.field_collection

    pydanclick.model.field_collection._is_pydantic_model = _is_pydantic_model


patch_pydanclick()


@click.group(cls=make_rst_to_ansi_formatter(DOC_URL, group=True))
@click.option("--url", help="The SCIM server endpoint.", envvar="SCIM_CLI_URL")
@click.option(
    "-h",
    "--header",
    multiple=True,
    type=HeaderType(),
    help="Headers to pass in the HTTP requests. Can be passed multiple times.",
    envvar="SCIM_CLI_HEADERS",
)
@click.pass_context
def cli(ctx, url: str, header: list[str]):
    """SCIM application development CLI."""
    ctx.ensure_object(dict)
    ctx.obj["URL"] = url
    headers_dict = split_headers(header)
    client = Client(base_url=ctx.obj["URL"], headers=headers_dict)
    ctx.obj["client"] = SyncSCIMClient(client, resource_models=(User, Group))
    ctx.obj["client"].register_naive_resource_types()
    ctx.obj["resource_models"] = {
        resource_model.__name__.lower(): resource_model
        for resource_model in ctx.obj["client"].resource_models
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
