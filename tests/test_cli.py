import json
import os

from scim2_models import AuthenticationScheme
from scim2_models import Bulk
from scim2_models import ChangePassword
from scim2_models import ETag
from scim2_models import Filter
from scim2_models import Patch
from scim2_models import ResourceType
from scim2_models import ServiceProviderConfig
from scim2_models import Sort
from scim2_models import User

from scim2_cli import cli


def test_no_url(runner):
    result = runner.invoke(cli, ["create"])
    assert result.exit_code == 1
    assert "No SCIM server URL defined.\n" in result.output


def test_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "SCIM application development CLI.\n" in result.output


def test_stdin_bad_json(runner, httpserver):
    """Test that invalid JSON stdin raise an error."""
    result = runner.invoke(
        cli,
        ["--url", httpserver.url_for("/"), "query", "user"],
        input="invalid",
        catch_exceptions=False,
    )
    assert result.exit_code == 1
    assert "Invalid JSON input." in result.stdout


def test_auth_headers(runner, httpserver, simple_user_payload):
    """Test passing auth bearer headers."""
    httpserver.expect_request(
        "/Users/foobar",
        method="GET",
        headers={"Authorization": "Bearer token", "foo": "bar"},
    ).respond_with_json(
        simple_user_payload("foobar"),
        status=200,
        content_type="application/scim+json",
    )

    result = runner.invoke(
        cli,
        [
            "--url",
            httpserver.url_for("/"),
            "query",
            "user",
            "foobar",
        ],
    )
    assert result.exit_code == 1

    result = runner.invoke(
        cli,
        [
            "--url",
            httpserver.url_for("/"),
            "--header",
            "Authorization: Bearer token",
            "--header",
            "foo: bar",
            "query",
            "user",
            "foobar",
        ],
    )
    assert result.exit_code == 0


def test_env_vars(runner, httpserver, simple_user_payload):
    """Test passing host and headers with environment vars."""
    httpserver.expect_request(
        "/Users/foobar",
        method="GET",
        headers={"Authorization": "Bearer token", "foo": "bar"},
    ).respond_with_json(
        simple_user_payload("foobar"),
        status=200,
        content_type="application/scim+json",
    )

    result = runner.invoke(cli, ["query", "user"])
    assert result.exit_code == 1

    os.environ["SCIM_CLI_URL"] = httpserver.url_for("/")
    os.environ["SCIM_CLI_HEADERS"] = "Authorization: Bearer token;foo: bar"
    try:
        result = runner.invoke(cli, ["query", "user", "foobar"], catch_exceptions=False)
        assert result.exit_code == 0
    finally:
        del os.environ["SCIM_CLI_URL"]
        del os.environ["SCIM_CLI_HEADERS"]


def test_custom_configuration(runner, httpserver, simple_user_payload, tmp_path):
    """Test passing custom .JSON configuration files to the command."""
    spc = ServiceProviderConfig(
        documentation_uri="https://scim.test",
        patch=Patch(supported=False),
        bulk=Bulk(supported=False, max_operations=0, max_payload_size=0),
        change_password=ChangePassword(supported=True),
        filter=Filter(supported=False, max_results=0),
        sort=Sort(supported=False),
        etag=ETag(supported=False),
        authentication_schemes=[
            AuthenticationScheme(
                name="OAuth Bearer Token",
                description="Authentication scheme using the OAuth Bearer Token Standard",
                spec_uri="http://www.rfc-editor.org/info/rfc6750",
                documentation_uri="https://scim.test",
                type="oauthbearertoken",
                primary=True,
            ),
        ],
    ).model_dump()

    spc_path = tmp_path / "service_provider_configuration.json"
    with open(spc_path, "w") as fd:
        json.dump(spc, fd)

    schemas = [User.to_schema().model_dump()]
    schemas_path = tmp_path / "schemas.json"
    with open(schemas_path, "w") as fd:
        json.dump(schemas, fd)

    resource_types = [
        ResourceType(
            id="User",
            name="User",
            endpoint="/somewhere-different",
            description="User accounts",
            schema_="urn:ietf:params:scim:schemas:core:2.0:User",
        ).model_dump()
    ]
    resource_types_path = tmp_path / "resource_types.json"
    with open(resource_types_path, "w") as fd:
        json.dump(resource_types, fd)

    httpserver.expect_request(
        "/somewhere-different/foobar",
        method="GET",
    ).respond_with_json(
        simple_user_payload("foobar"),
        status=200,
        content_type="application/scim+json",
    )

    result = runner.invoke(
        cli,
        [
            "--url",
            httpserver.url_for("/"),
            "--service-provider-config",
            spc_path,
            "--schemas",
            schemas_path,
            "--resource-types",
            resource_types_path,
            "query",
            "user",
            "foobar",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
