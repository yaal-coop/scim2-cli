import json

import click
import requests
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

DOC_URL = "https://scim2-cli.readthedocs.io/"
BASE_HEADERS = {
    "Accept": "application/scim+json",
    "Content-Type": "application/scim+json",
}


@click.group(cls=make_rst_to_ansi_formatter(DOC_URL, group=True))
@click.argument("url")
@click.pass_context
def cli(ctx, url):
    """SCIM application development CLI."""
    ctx.ensure_object(dict)
    ctx.obj["URL"] = url

    if not click.get_text_stream("stdin").isatty():  # pragma: no cover
        stdin = click.get_text_stream("stdin").read().strip()
        ctx.obj["STDIN"] = json.loads(stdin)


@cli.command(cls=make_rst_to_ansi_formatter(DOC_URL))
@click.pass_context
def get(ctx):
    """Perform a `SCIM GET <https://www.rfc-editor.org/rfc/rfc7644#section-3.4.1>`_ request.

    Data passed in JSON format to stdin is sent as request arguments:

    .. code-block:: bash

        echo '{"foo": "bar"}' | scim https://scim.example get
    """

    response = requests.get(
        ctx.obj["URL"],
        params=ctx.obj.get("STDIN"),
        headers=BASE_HEADERS,
        allow_redirects=True,
    )
    click.echo(response.text)


@cli.command(cls=make_rst_to_ansi_formatter(DOC_URL))
@click.pass_context
def post(ctx):
    """Perform a `SCIM POST <https://www.rfc-editor.org/rfc/rfc7644#section-3.3>`_ request.

    Data passed in JSON format to stdin is sent as request payload:

    .. code-block:: bash

        echo '{"foo": "bar"}' | scim https://scim.example post
    """

    response = requests.post(
        ctx.obj["URL"],
        json=ctx.obj.get("STDIN"),
        headers=BASE_HEADERS,
        allow_redirects=True,
    )
    click.echo(response.text)


@cli.command(cls=make_rst_to_ansi_formatter(DOC_URL))
@click.pass_context
def put(ctx):
    """Perform a `SCIM PUT <https://www.rfc-editor.org/rfc/rfc7644#section-3.5.1>`_ request.

    Data passed in JSON format to stdin is sent as request payload:

    .. code-block:: bash

        echo '{"foo": "bar"}' | scim https://scim.example put
    """

    response = requests.put(
        ctx.obj["URL"],
        json=ctx.obj.get("STDIN"),
        headers=BASE_HEADERS,
        allow_redirects=True,
    )
    click.echo(response.text)


@cli.command(cls=make_rst_to_ansi_formatter(DOC_URL))
@click.pass_context
def patch(ctx):
    """Perform a `SCIM PATCH <https://www.rfc-editor.org/rfc/rfc7644#section-3.5.2>`_ request.

    Data passed in JSON format to stdin is sent as request payload:

    .. code-block:: bash

        echo '{"foo": "bar"}' | scim https://scim.example patch
    """

    response = requests.patch(
        ctx.obj["URL"],
        json=ctx.obj.get("STDIN"),
        headers=BASE_HEADERS,
        allow_redirects=True,
    )
    click.echo(response.text)


@cli.command(cls=make_rst_to_ansi_formatter(DOC_URL))
@click.pass_context
def delete(ctx):
    """Perform a `SCIM DELETE <https://www.rfc-editor.org/rfc/rfc7644#section-3.6>`_ request.

    Data passed in JSON format to stdin is sent as request payload:

    .. code-block:: bash

        echo '{"foo": "bar"}' | scim https://scim.example delete
    """

    response = requests.delete(
        ctx.obj["URL"],
        json=ctx.obj.get("STDIN"),
        headers=BASE_HEADERS,
        allow_redirects=True,
    )
    click.echo(response.text)
