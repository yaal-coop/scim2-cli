Tutorial
========

The :ref:`cli` command allows you to interact with a SCIM server.

Basic parameters
----------------

In order to connect to a SCIM server you will need to pass the :option:`scim --url` parameter.
You can also pass additional headers, such as authentication ones, with :option:`scim --url`.

.. code-block:: shell

    $ scim2 --url https://auth.example --header "Authorization: Bearer 12345" create user --user-name "bjensen@example.com"
    {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "2819c223-7f76-453a-919d-413861904646",
        "userName": "bjensen@example.com",
        "meta": {
            "resourceType": "User",
            "created": "2010-01-23T04:56:22Z",
            "lastModified": "2011-05-13T04:42:34Z",
            "version": 'W\\/"3694e05e9dff590"',
            "location": "https://example.com/v2/Users/2819c223-7f76-453a-919d-413861904646",
        },
    }

However passing those parameters each time you use the command can be annoying.
To make commands shorter, you can set those parameters once for all by using the :ref:`SCIM_CLI_URL <scim-url-scim_cli_url>` and :ref:`SCIM_CLI_HEADERS <scim-header-scim_cli_headers>` environment vars.

.. code-block:: shell

    $ export SCIM_CLI_URL="https://auth.example"
    $ export SCIM_CLI_HEADERS="Authorization: Bearer 12345"
    $ scim2 create user --user-name "bjensen@example.com"
    {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": "2819c223-7f76-453a-919d-413861904646",
        "userName": "bjensen@example.com",
        "meta": {
            "resourceType": "User",
            "created": "2010-01-23T04:56:22Z",
            "lastModified": "2011-05-13T04:42:34Z",
            "version": 'W\\/"3694e05e9dff590"',
            "location": "https://example.com/v2/Users/2819c223-7f76-453a-919d-413861904646",
        },
    }
