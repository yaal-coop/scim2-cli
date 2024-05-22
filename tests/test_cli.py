import json

from scim_cli import cli


def test_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "SCIM application development CLI.\n" in result.output


def test_get_stdin(runner, echoserver):
    """Test that JSON stdin is passed in the GET request."""
    payload = {"foo": "bar"}
    result = runner.invoke(
        cli,
        [echoserver.url_for("/"), "get"],
        input=json.dumps(payload),
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    expected_payload = {"method": "GET", "args": payload}
    json_output = json.loads(result.output)
    assert expected_payload == json_output


def test_post_stdin(runner, echoserver):
    """Test that JSON stdin is passed in the POST request."""

    payload = {"foo": "bar"}
    result = runner.invoke(
        cli,
        [echoserver.url_for("/"), "post"],
        input=json.dumps(payload),
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    expected_payload = {"method": "POST", "payload": payload}
    json_output = json.loads(result.output)
    assert expected_payload == json_output


def test_put_stdin(runner, echoserver):
    """Test that JSON stdin is passed in the PUT request."""

    payload = {"foo": "bar"}
    result = runner.invoke(
        cli,
        [echoserver.url_for("/"), "put"],
        input=json.dumps(payload),
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    expected_payload = {"method": "PUT", "payload": payload}
    json_output = json.loads(result.output)
    assert expected_payload == json_output


def test_patch_stdin(runner, echoserver):
    """Test that JSON stdin is passed in the POST request."""

    payload = {"foo": "bar"}
    result = runner.invoke(
        cli,
        [echoserver.url_for("/"), "patch"],
        input=json.dumps(payload),
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    expected_payload = {"method": "PATCH", "payload": payload}
    json_output = json.loads(result.output)
    assert expected_payload == json_output


def test_delete_stdin(runner, echoserver):
    """Test that JSON stdin is passed in the DELETE request."""
    payload = {"foo": "bar"}
    result = runner.invoke(
        cli,
        [echoserver.url_for("/"), "delete"],
        input=json.dumps(payload),
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    expected_payload = {"method": "DELETE", "payload": payload}
    json_output = json.loads(result.output)
    assert expected_payload == json_output
