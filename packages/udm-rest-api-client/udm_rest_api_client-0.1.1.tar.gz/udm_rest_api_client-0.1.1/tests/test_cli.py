# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import subprocess
import uuid


# Importing "from univention.admin.rest.client.__main__ import main" and calling main(udm_cli_conn_settings + ["users/user"] ...) works,
# but although Pytest captures STDOUT its content is not available in capsys or capfd. Thus, subprocess.run().


def test_cli_user_create(capfd, delete_foo_users_after_test, udm_cli_conn_settings) -> None:
    username = f"foo_{uuid.uuid4().hex[:10]}"
    lastname = f"ln_{uuid.uuid4().hex[:10]}"
    password = uuid.uuid4().hex
    capfd.readouterr()  # reset buffer

    subprocess.run(["udm"] + udm_cli_conn_settings + ["users/user", "create", "--set", f"username={username}", "--set", f"lastname={lastname}", "--set", f"password={password}"])

    captured = capfd.readouterr()
    assert f"Object created: uid={username}" in captured.out


def test_cli_user_list(capfd, delete_foo_users_after_test, udm_cli_conn_settings, udm_rest_connection_settings) -> None:
    username = f"foo_{uuid.uuid4().hex[:10]}"
    lastname = f"ln_{uuid.uuid4().hex[:10]}"
    password = uuid.uuid4().hex
    uri = udm_rest_connection_settings["uri"]

    subprocess.run(["udm"] + udm_cli_conn_settings + ["users/user", "create", "--set", f"username={username}", "--set", f"lastname={lastname}", "--set", f"password={password}"])
    capfd.readouterr()  # reset buffer

    subprocess.run(["udm"] + udm_cli_conn_settings + ["users/user", "list", "--filter", f"uid={username}"])

    captured = capfd.readouterr()
    assert f"DN: uid={username},cn=users," in captured.out
    assert f"URL: {uri.rstrip('/')}/users/user/uid%3D{username}%2Ccn%3Dusers%2C" in captured.out
    assert "Object-Type: users/user" in captured.out
    assert f"lastname: {lastname}" in captured.out
    assert f"username: {username}" in captured.out
