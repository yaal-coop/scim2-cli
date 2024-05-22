from scim_cli import cli


def test_hello_world(runner):
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert result.output == "Hello world!\n"
