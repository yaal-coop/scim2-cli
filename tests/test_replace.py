import json

from scim2_cli import cli


def test_stdin(runner, httpserver, simple_user_payload):
    """Test that JSON stdin is passed in the PUT request."""

    response_payload = simple_user_payload("old-user")
    httpserver.expect_request(
        "/Users/old-user",
        method="PUT",
    ).respond_with_json(
        response_payload,
        status=200,
        content_type="application/scim+json",
    )

    payload = {
        "id": "old-user",
        "schemas": [
            "urn:ietf:params:scim:schemas:core:2.0:User",
        ],
        "userName": "old-user@example.com",
    }

    result = runner.invoke(
        cli,
        [httpserver.url_for("/"), "replace"],
        input=json.dumps(payload),
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.stdout
    json_output = json.loads(result.output)

    assert json_output == response_payload


def test_payload_without_an_id(runner, httpserver, simple_user_payload):
    """Test that ids are needed."""

    payload = {
        "schemas": [
            "urn:ietf:params:scim:schemas:core:2.0:User",
        ],
        "userName": "old-user@example.com",
    }

    result = runner.invoke(
        cli,
        [httpserver.url_for("/"), "replace"],
        input=json.dumps(payload),
        catch_exceptions=False,
    )
    assert result.exit_code == 1, result.stdout
    assert "Resource must have an id" in result.stdout


def test_no_stdin(runner, httpserver, simple_user_payload):
    """Test missing stdin."""

    result = runner.invoke(
        cli,
        [httpserver.url_for("/"), "replace"],
        catch_exceptions=False,
    )
    assert result.exit_code == 1, result.stdout
    assert "Input data is missing" in result.stdout


def test_scimclient_error(runner, httpserver, simple_user_payload):
    """Test scim2_client errors handling."""

    httpserver.expect_request(
        "/Users/old-user",
        method="PUT",
    ).respond_with_json(
        simple_user_payload("old-user"),
        status=999,
        content_type="application/scim+json",
    )

    payload = {
        "id": "old-user",
        "schemas": [
            "urn:ietf:params:scim:schemas:core:2.0:User",
        ],
        "userName": "old-user@example.com",
    }

    result = runner.invoke(
        cli,
        [
            httpserver.url_for("/"),
            "replace",
        ],
        input=json.dumps(payload),
        catch_exceptions=False,
    )
    assert result.exit_code == 1, result.stdout
    assert "Unexpected response status code: 999" in result.stdout


def test_validation_error(runner, httpserver, simple_user_payload):
    """Test pydantic errors handling."""

    httpserver.expect_request(
        "/Users/old-user",
        method="PUT",
    ).respond_with_json(
        {"invalid": "json"},
        status=200,
        content_type="application/scim+json",
    )

    payload = {
        "id": "old-user",
        "schemas": [
            "urn:ietf:params:scim:schemas:core:2.0:User",
        ],
        "userName": "old-user@example.com",
    }

    result = runner.invoke(
        cli,
        [
            httpserver.url_for("/"),
            "replace",
        ],
        catch_exceptions=False,
        input=json.dumps(payload),
    )
    assert result.exit_code == 1, result.stdout
    assert "Expected type User but got undefined object with no schema" in result.stdout
