from scim2_models import Context
from scim2_models import GroupMember
from scim2_models import User

from scim2_cli.utils import is_field_acceptable


def test_is_field_acceptable():
    assert is_field_acceptable(Context.RESOURCE_CREATION_REQUEST, User, "user_name")
    assert not is_field_acceptable(Context.RESOURCE_CREATION_REQUEST, User, "id")

    assert is_field_acceptable(Context.RESOURCE_QUERY_REQUEST, User, "user_name")
    assert not is_field_acceptable(Context.RESOURCE_QUERY_REQUEST, User, "password")

    assert is_field_acceptable(Context.SEARCH_REQUEST, User, "user_name")
    assert not is_field_acceptable(Context.SEARCH_REQUEST, User, "password")

    assert is_field_acceptable(Context.RESOURCE_REPLACEMENT_REQUEST, User, "password")
    assert not is_field_acceptable(
        Context.RESOURCE_REPLACEMENT_REQUEST, GroupMember, "type"
    )
