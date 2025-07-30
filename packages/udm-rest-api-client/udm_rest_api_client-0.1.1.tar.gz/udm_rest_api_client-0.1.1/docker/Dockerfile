# syntax=docker/dockerfile:1.9
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=0.17.3-build-2025-05-11
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-python-521

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}
SHELL ["/bin/bash", "-uxo", "pipefail", "-c"]

ENV PYTHONUNBUFFERED=1

WORKDIR /udm-rest-api-client
COPY docker/test-entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

RUN rm -fv /usr/lib/python*/EXTERNALLY-MANAGED && \
    apt-get --assume-yes --verbose-versions --no-install-recommends install python3-ldap python3-pip && \
    rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY pyproject.toml README.md /udm-rest-api-client/
COPY debian/changelog /udm-rest-api-client/debian/
COPY src /udm-rest-api-client/src/
COPY tests /udm-rest-api-client/tests/

RUN pip3 install --break-system-packages --compile --no-cache-dir --editable '.[async,cli,dev,sync]' && \
    python3 -c 'from univention.admin.rest.client import UDM' && \
    python3 -c 'from univention.admin.rest.async_client import UDM' && \
    udm --help
