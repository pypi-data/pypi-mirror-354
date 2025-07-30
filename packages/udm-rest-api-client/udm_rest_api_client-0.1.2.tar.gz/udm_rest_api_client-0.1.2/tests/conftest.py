import os
from collections.abc import AsyncGenerator

import pytest

from univention.admin.rest.async_client import UDM as AUDM
from univention.admin.rest.client import UDM


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
    module = udm_sync.get("users/user")

    for result in module.search("uid=foo*"):
        obj = result.open()
        obj.delete()


@pytest.fixture
def udm_cli_conn_settings(tmp_path, udm_rest_connection_settings) -> list[str]:
    pw_file = tmp_path / "udm_password"
    with pw_file.open("w") as fp:
        fp.write(udm_rest_connection_settings["password"])
    return ["--username", udm_rest_connection_settings["username"], "--bindpwdfile", str(pw_file), "--uri", udm_rest_connection_settings["uri"]]
