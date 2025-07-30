#!/bin/bash
 # SPDX-License-Identifier: AGPL-3.0-only
 # SPDX-FileCopyrightText: 2025 Univention GmbH

sleep 10  # wait for LDAP and UDM REST servers to become ready
pytest
coverage xml --ignore-errors
