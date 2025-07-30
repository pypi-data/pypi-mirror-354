# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest

from univention.admin.rest.async_client import UDM as AUDM
from univention.admin.rest.client import UDM, UnprocessableEntity


def test_readme_sync(udm_sync: UDM, delete_foo_users_after_test):
    module = udm_sync.get("users/user")

    print("# 1. create a user")
    obj1 = module.new()
    obj1.properties["username"] = "foo"
    obj1.properties["password"] = "univention"
    obj1.properties["lastname"] = "foo"
    obj1.save()

    print("# 2. search for users")
    for result in module.search("uid=*"):
        assert getattr(result, "dn", "").startswith("uid=foo")
        obj2 = result.open()
        print(obj2)
        print(obj2.properties)
        print(obj2.objects.groups)
        if obj2.properties["username"] == "foo":
            print("Found user 'foo'.")
            break
    else:
        raise AssertionError("User 'foo' not found.")  # pragma: no cover

    print("# 3. get by dn")
    ldap_base = udm_sync.get_ldap_base()
    obj3 = module.get(f"uid=foo,cn=users,{ldap_base}")
    assert obj3

    print("# 4. get referenced objects e.g. groups")
    pg = obj3.objects["primaryGroup"][0].open()
    print(pg.dn, pg.properties)
    print(obj3.objects["groups"])
    assert pg.properties["name"] == "Domain Users"

    print("# 5. modify")
    obj3.properties["description"] = "foo"
    obj3.save()
    assert module.get(f"uid=foo,cn=users,{ldap_base}").properties["description"] == "foo"

    print("# 6. move to the ldap base")
    obj3.move(ldap_base)
    assert module.get(f"uid=foo,{ldap_base}")

    print("# 7. remove")
    obj3.delete()
    with pytest.raises(UnprocessableEntity):  # FIXME: Should be NotFound
        module.get(f"uid=foo,{ldap_base}")


@pytest.mark.asyncio
async def test_readme_async(udm_async: AUDM, delete_foo_users_after_test):
    module = await udm_async.get("users/user")

    print("# 1. create a user")
    obj1 = await module.new()
    obj1.properties["username"] = "foo_async"
    obj1.properties["password"] = "univention"
    obj1.properties["lastname"] = "foo_async"
    await obj1.save()

    print("# 2. search for users")
    async for result in module.search("uid=*"):
        assert getattr(result, "dn", "").startswith("uid=foo_async")
        obj2 = await result.open()
        print(obj2)
        print(obj2.properties)
        print(obj2.objects.groups)
        if obj2.properties["username"] == "foo_async":
            print("Found user 'foo_async'.")
            break
    else:
        raise AssertionError("User 'foo_async' not found.")  # pragma: no cover

    print("# 3. get by dn")
    ldap_base = await udm_async.get_ldap_base()
    obj3 = await module.get(f"uid=foo_async,cn=users,{ldap_base}")
    assert obj3

    print("# 4. get referenced objects e.g. groups")
    pg = await obj3.objects["primaryGroup"][0].open()
    print(pg.dn, pg.properties)
    print(obj3.objects["groups"])
    assert pg.properties["name"] == "Domain Users"

    print("# 5. modify")
    obj3.properties["description"] = "foo_async"
    await obj3.save()
    assert (await module.get(f"uid=foo_async,cn=users,{ldap_base}")).properties["description"] == "foo_async"

    print("# 6. move to the ldap base")
    await obj3.move(ldap_base)
    assert await module.get(f"uid=foo_async,{ldap_base}")

    print("# 7. remove")
    await obj3.delete()
    with pytest.raises(UnprocessableEntity):  # FIXME: Should be NotFound
        await module.get(f"uid=foo_async,{ldap_base}")
