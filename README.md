# scim2-cli

An utility command line to help you perform requests against a SCIM server, while validating input and response payloads.

## Installation

```shell
pip install scim2-cli
```

## Usage

Check the [reference](https://scim2-cli.readthedocs.io/en/latest/reference.html) for more details.

Here is an example of resource creation:

```shell
$ scim2 https://auth.example create user << EOL
{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
    "userName": "bjensen@example.com"
}
EOL
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
```

Here is an example of resource query:

```shell
$ scim2 https://auth.example query user 2819c223-7f76-453a-919d-413861904646
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
   }
}
```
