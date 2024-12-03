from scim2_cli import cli


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
    )
    assert result.exit_code == 1
    assert "Invalid JSON input." in result.stdout


def test_auth_headers(runner, httpserver, simple_user_payload):
    """Test passing auth bearer headers."""
    httpserver.expect_request(
        "/Users/foobar", method="GET", headers={"Authorization": "Bearer token"}
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
            "--headers",
            "Authorization: Bearer token",
            "query",
            "user",
            "foobar",
        ],
    )
    assert result.exit_code == 0
