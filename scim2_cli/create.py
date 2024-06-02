import click
import httpx
from click import ClickException
from pydantic import ValidationError
from scim2_client import SCIMClientError
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

from .utils import DOC_URL
from .utils import formatted_payload


@click.command(cls=make_rst_to_ansi_formatter(DOC_URL), name="create")
@click.pass_context
@click.option(
    "--indent/--no-indent",
    is_flag=True,
    default=True,
    help="Indent JSON response payloads.",
)
def create_cli(ctx, indent):
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
        response = ctx.obj["client"].create(payload)

    except (httpx.HTTPError, SCIMClientError) as exc:
        raise ClickException(exc) from exc

    except ValidationError as exc:
        payload = formatted_payload(exc.response_payload, indent)
        message = f"The server response is invalid:\n{payload}\n{exc}"
        raise ClickException(message) from exc

    payload = formatted_payload(response.model_dump(), indent)
    click.echo(payload)
