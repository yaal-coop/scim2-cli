import sys

import click
from click import ClickException
from scim2_client import SCIMClientError
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

from .utils import DOC_URL
from .utils import formatted_payload
from .utils import split_headers


@click.command(cls=make_rst_to_ansi_formatter(DOC_URL), name="create")
@click.pass_context
@click.option(
    "--indent/--no-indent",
    is_flag=True,
    default=True,
    help="Indent JSON response payloads.",
)
@click.option(
    "-h", "--headers", multiple=True, help="Header to pass in the HTTP requests."
)
def create_cli(ctx, indent, headers):
    """Perform a `SCIM POST <https://www.rfc-editor.org/rfc/rfc7644#section-3.3>`_ request
    on resources endpoint.

    Input data is expected to be passed in JSON format to stdin:

    .. code-block:: bash

        echo '{"userName": "bjensen@example.com", "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"]}' | scim https://scim.example create user

    """

    payload = ctx.obj.get("stdin")
    if not payload:
        raise ClickException("Input data is missing")

    try:
        response = ctx.obj["client"].create(payload, headers=split_headers(headers))

    except SCIMClientError as scim_exc:
        message = str(scim_exc)
        if sys.version_info >= (3, 11) and hasattr(
            scim_exc, "__notes__"
        ):  # pragma: no cover
            for note in scim_exc.__notes__:
                message = f"{message}\n{note}"
        raise ClickException(message) from scim_exc

    payload = formatted_payload(response.model_dump(), indent)
    click.echo(payload)
