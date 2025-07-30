import os
from collections.abc import AsyncGenerator

import pytest

from univention.admin.rest.async_client import UDM as AUDM
from univention.admin.rest.client import UDM, NotFound, UnprocessableEntity


@pytest.fixture(scope="session")
def udm_rest_connection_settings() -> dict[str, str]:
    return {
        "uri": os.environ.get("UDM_URL", "http://udm-rest-api:9979/udm/"),
        "username": os.environ.get("UDM_USERNAME", "cn=admin"),
        "password": os.environ.get("UDM_PASSWORD", "univention"),
    }


@pytest.fixture
def udm_sync(udm_rest_connection_settings) -> UDM:
    print(f"Connecting sync to {udm_rest_connection_settings!r}...")
    return UDM.http(**udm_rest_connection_settings)


@pytest.fixture
async def udm_async(udm_rest_connection_settings) -> AsyncGenerator[AUDM, None]:
    print(f"Connecting async to {udm_rest_connection_settings!r}...")
    async with AUDM.http(**udm_rest_connection_settings) as udm:
        yield udm


@pytest.fixture
def delete_foo_users_after_test(udm_sync):
    yield
    ldap_base = udm_sync.get_ldap_base()
    module = udm_sync.get("users/user")

    for dn in (f"uid=foo,{ldap_base}", f"uid=foo,cn=users,{ldap_base}", f"uid=foo_async,{ldap_base}", f"uid=foo_async,cn=users,{ldap_base}"):
        try:
            obj = module.get(dn)
            obj.delete()
            print(f"Deleted user {dn!r}.")
        except (NotFound, UnprocessableEntity):
            pass
