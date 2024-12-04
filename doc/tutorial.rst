Tutorial
========

The :ref:`cli` command allows you to interact with a SCIM server.

Basic parameters
----------------

In order to connect to a SCIM server you will need to pass the :option:`--url <scim --url>` parameter.
You can also pass additional headers, such as authentication ones, with :option:`--header <scim --header>`.

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


Server configuration
--------------------

The CLI needs to reach the server configuration to find out which features are available,
which resource schemas are available, and where they are located.

By default the CLI will automatically discover those resources on the server, before each command is run.

However you might find too time consuming to achieve all those network requests.
You can store those data locally and reuse them for future command runs thanks to the
:option:`--schemas <scim --schemas>`, :option:`--resource-types <scim --resource-types>` and :option:`--service-provider-config <scim --service-provider-config>` (and their corresponding environment vars :ref:`SCIM_CLI_SCHEMAS <scim-schemas-scim_cli_schemas>`, :ref:`SCIM_CLI_RESOURCE_TYPES <scim-resource_types-scim_cli_resource_types>` and :ref:`SCIM_CLI_SERVICE_PROVIDER_CONFIG <scim-service_provider_config-scim_cli_service_provider_config>`)

.. code-block:: shell
    :caption: Save the configuration resources

    $ scim query schema > /tmp/schemas.json
    $ scim query resourcetype > /tmp/resource-types.json
    $ scim query serviceproviderconfig > /tmp/service-provider-config.json

.. code-block:: shell
    :caption: Load the cached resources

    $ export SCIM_SCHEMAS=/tmp/schemas.json
    $ export SCIM_RESOURCE_TYPES=/tmp/resource-types.json
    $ export SCIM_SERVICE_PROVIDER_CONFIG=/tmp/service-provider-config.json
    $ scim2 query ...
