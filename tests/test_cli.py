from scim2_cli import cli


def test_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "SCIM application development CLI.\n" in result.output


def test_stdin_bad_json(runner, httpserver):
    """Test that invalid JSON stdin raise an error."""
    result = runner.invoke(
        cli,
        [httpserver.url_for("/"), "query", "user"],
        input="invalid",
    )
    assert result.exit_code == 1
    assert "Invalid JSON input." in result.stdout
