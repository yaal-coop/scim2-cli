import pytest
from click.testing import CliRunner
from scim2_models import AuthenticationScheme
from scim2_models import Bulk
from scim2_models import ChangePassword
from scim2_models import ETag
from scim2_models import Filter
from scim2_models import ListResponse
from scim2_models import Patch
from scim2_models import ResourceType
from scim2_models import Schema
from scim2_models import ServiceProviderConfig
from scim2_models import Sort
from scim2_models import User


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def httpserver(httpserver):
    httpserver.expect_request("/ServiceProviderConfig").respond_with_json(
        ServiceProviderConfig(
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
        ).model_dump(),
        status=200,
        content_type="application/scim+json",
    )

    httpserver.expect_request("/ResourceTypes").respond_with_json(
        ListResponse[ResourceType](
            total_results=1,
            start_index=1,
            items_per_page=1,
            resources=[
                ResourceType(
                    name="User",
                    id="User",
                    endpoint="/Users",
                    schema_="urn:ietf:params:scim:schemas:core:2.0:User",
                )
            ],
        ).model_dump(),
        status=200,
        content_type="application/scim+json",
    )

    httpserver.expect_request("/Schemas").respond_with_json(
        ListResponse[Schema](
            total_results=1,
            start_index=1,
            items_per_page=1,
            resources=[User.to_schema()],
        ).model_dump(),
        status=200,
        content_type="application/scim+json",
    )

    return httpserver


@pytest.fixture
def simple_user_payload(httpserver):
    def wrapped(id):
        return {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": id,
            "userName": f"{id}@example.com",
            "meta": {
                "resourceType": "User",
                "created": "2010-01-23T04:56:22Z",
                "lastModified": "2011-05-13T04:42:34Z",
                "version": 'W\\/"3694e05e9dff590"',
                "location": f"http://localhost:{httpserver.port}/Users/{id}",
            },
        }

    return wrapped
