import click
from scim2_tester import Status
from scim2_tester import check_server
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

from .utils import DOC_URL
from .utils import Color
from .utils import split_headers


@click.command(cls=make_rst_to_ansi_formatter(DOC_URL), name="test")
@click.pass_context
@click.option(
    "-h", "--headers", multiple=True, help="Header to pass in the HTTP requests."
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
def test_cli(ctx, headers, verbose):
    """Perform a server SCIM compliance check using :doc:`scim2-tester
    <scim2-tester:index>`.

    .. code-block:: bash

        scim https://scim.example test
    """

    client = ctx.obj["client"]
    client.client.headers.update(split_headers(headers))
    results = check_server(client)
    click.echo(f"Performing a SCIM compliance check on {client.client.base_url} ...")
    for result in results:
        if result.status == Status.SUCCESS:
            status = click.style(result.status.name, fg=Color.green)
        else:
            status = click.style(result.status.name, fg=Color.red)
        click.echo(f"{status} {result.title}")

        if result.reason:
            click.echo(f"  {result.reason}")
            if verbose and result.data:
                click.echo(f"  {result.data}")
