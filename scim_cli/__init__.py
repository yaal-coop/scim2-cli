import json

import click
import requests

BASE_HEADERS = {
    "Accept": "application/scim+json",
    "Content-Type": "application/scim+json",
}


@click.group()
@click.argument("url")
@click.pass_context
def cli(ctx, url):
    """SCIM application development CLI."""
    ctx.ensure_object(dict)
    ctx.obj["URL"] = url

    if not click.get_text_stream("stdin").isatty():  # pragma: no cover
        stdin = click.get_text_stream("stdin").read().strip()
        ctx.obj["STDIN"] = json.loads(stdin)


@cli.command()
@click.pass_context
def get(ctx):
    """Perform a SCIM GET request.

    Data passed in JSON format to stdin is sent as request arguments::

        echo '{"foo": "bar"}' | scim https://scim.example get

    Details on: https://www.rfc-editor.org/rfc/rfc7644#section-3.4.1
    """

    response = requests.get(
        ctx.obj["URL"],
        params=ctx.obj.get("STDIN"),
        headers=BASE_HEADERS,
        allow_redirects=True,
    )
    click.echo(response.text)


@cli.command()
@click.pass_context
def post(ctx):
    """Perform a SCIM POST request.

    Data passed in JSON format to stdin is sent as request payload::

        echo '{"foo": "bar"}' | scim https://scim.example post

    https://www.rfc-editor.org/rfc/rfc7644#section-3.3
    """

    response = requests.post(
        ctx.obj["URL"],
        json=ctx.obj.get("STDIN"),
        headers=BASE_HEADERS,
        allow_redirects=True,
    )
    click.echo(response.text)


@cli.command()
@click.pass_context
def put(ctx):
    """Perform a SCIM PUT request.

    Data passed in JSON format to stdin is sent as request payload::

        echo '{"foo": "bar"}' | scim https://scim.example put

    https://www.rfc-editor.org/rfc/rfc7644#section-3.5.1
    """

    response = requests.put(
        ctx.obj["URL"],
        json=ctx.obj.get("STDIN"),
        headers=BASE_HEADERS,
        allow_redirects=True,
    )
    click.echo(response.text)


@cli.command()
@click.pass_context
def patch(ctx):
    """Perform a SCIM PATCH request.

    Data passed in JSON format to stdin is sent as request payload::

        echo '{"foo": "bar"}' | scim https://scim.example patch

    https://www.rfc-editor.org/rfc/rfc7644#section-3.5.2
    """

    response = requests.patch(
        ctx.obj["URL"],
        json=ctx.obj.get("STDIN"),
        headers=BASE_HEADERS,
        allow_redirects=True,
    )
    click.echo(response.text)


@cli.command()
@click.pass_context
def delete(ctx):
    """Perform a SCIM DELETE request.

    Data passed in JSON format to stdin is sent as request payload::

        echo '{"foo": "bar"}' | scim https://scim.example delete

    https://www.rfc-editor.org/rfc/rfc7644#section-3.6
    """

    response = requests.delete(
        ctx.obj["URL"],
        json=ctx.obj.get("STDIN"),
        headers=BASE_HEADERS,
        allow_redirects=True,
    )
    click.echo(response.text)
