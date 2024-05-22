import json

import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def echoserver(httpserver):
    def echo_handler(request):
        payload = {
            "method": request.method,
        }

        if request.args:
            payload["args"] = request.args

        if request.data:
            payload["payload"] = request.json if request.is_json else request.data

        return json.dumps(payload)

    httpserver.expect_request("/").respond_with_handler(echo_handler)
    return httpserver
