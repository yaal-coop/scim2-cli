import sys

import click
from click import ClickException
from pydanclick import from_pydantic
from scim2_client import SCIMClientError
from scim2_models import Context
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

from .utils import DOC_URL
from .utils import ModelCommand
from .utils import formatted_payload
from .utils import unacceptable_fields


def replace_payload(client, payload, indent):
    try:
        response = client.replace(payload, raise_scim_errors=False)

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


def replace_factory(model):
    exclude = unacceptable_fields(Context.RESOURCE_REPLACEMENT_REQUEST, model)
    exclude.remove("id")

    @click.command(
        cls=make_rst_to_ansi_formatter(DOC_URL),
        name=model.__name__.lower(),
    )
    @click.option(
        "--indent/--no-indent",
        is_flag=True,
        default=True,
        help="Indent JSON response payloads.",
    )
    @from_pydantic("obj", model, exclude=exclude)
    @click.pass_context
    def replace_command(ctx, indent, obj: model, *args, **kwargs):
        r"""Perform a `SCIM PUT <https://www.rfc-editor.org/rfc/rfc7644#section-3.3>`_ request on resources endpoint.

        Input data can be passed through parameters like :code:`--external-id`.

        .. code-block:: bash

            scim https://scim.example replace user --id "xxxx-yyyy" --user-name "foo" --name-given-name "bar"

        Multiple attributes should be passed as JSON payloads:

        .. code-block:: bash

            scim https://scim.example replace user \\
                --id "xxxx-yyyy" \\
                --user-name "foo" \\
                --emails '[{"value":"foo@bar.example", "primary": true}, {"value": "foo@baz.example"}]'

        Input can also be passed through stdin in JSON format:

        .. code-block:: bash

            echo '{"id": "xxxx-yyyy", "userName": "bjensen@example.com", "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"]}' | scim https://scim.example replace user

        """
        if obj == model():
            obj = None

        payload = ctx.obj.get("stdin") or obj
        if not payload:
            click.echo(ctx.get_help())
            ctx.exit(1)

        replace_payload(
            ctx.obj["client"],
            payload,
            indent,
        )

    return replace_command


@click.command(
    cls=ModelCommand,
    factory=replace_factory,
    name="replace",
    invoke_without_command=True,
)
@click.pass_context
@click.option(
    "--indent/--no-indent",
    is_flag=True,
    default=True,
    help="Indent JSON response payloads.",
)
def replace_cli(ctx, indent):
    """Perform a `SCIM PUT <https://www.rfc-editor.org/rfc/rfc7644#section-3.5.1>`_ request on the resources endpoint.

    There are subcommands for all the available models, with dynamic attributes.
    See the attributes for :code:`user` with:

    .. code-block:: bash

        scim https://scim.example replace user --help

    If no subcommand is executed, input data is expected to be passed in JSON format to stdin:

    .. code-block:: bash

        echo '{"userName": "bjensen@example.com", "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"], "id": "1234"}' | scim https://scim.example replace user

    """
    if ctx.invoked_subcommand is not None:
        return

    payload = ctx.obj.get("stdin")
    if not payload:
        click.echo(ctx.get_help())
        ctx.exit(1)

    replace_payload(
        ctx.obj["client"],
        payload,
        indent,
    )
