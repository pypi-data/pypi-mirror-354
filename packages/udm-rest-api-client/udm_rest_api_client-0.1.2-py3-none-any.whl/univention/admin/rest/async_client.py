#!/usr/bin/python3
#
# Univention Directory Manager
#  REST API async client
#
# Like what you see? Join us!
# https://www.univention.com/about-us/careers/vacancies/
#
# SPDX-FileCopyrightText: 2019-2025 Univention GmbH
# SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-Univention-Proprietary

"""
Sample asynchronous client for the UDM REST API.

```python
import asyncio
from univention.admin.rest.async_client import UDM
uri = 'http://localhost/univention/udm/'

async def main():
    async with UDM.http(uri, 'Administrator', 'univention') as udm:
        module = await udm.get('users/user')
        print(f'Found {module}')
        objs = module.search()
        async for obj in objs:
            if not obj:
                continue
            obj = await obj.open()
            print(f'Object {obj}')
            for group in obj.objects.groups:
                grp = await group.open()
                print(f'Group {grp}')

asyncio.run(main())
```
"""

from __future__ import annotations

import asyncio
import contextlib
import copy
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator, Mapping
from types import TracebackType
from typing import Any, TypeVar, cast

import aiohttp
import uritemplate
from typing_extensions import Protocol

from .client import (
    BadRequest,
    ConnectionError,
    Forbidden,
    HTTPError,
    HttpRequestP,
    HttpResponse,
    NoRelation,
    NotFound,
    ObjectCopyProto,
    ObjectRepr,
    PreconditionFailed,
    References as SyncReferences,
    Response,
    ServerError,
    ServiceUnavailable,
    Unauthorized,
    UnexpectedResponse,
    UnprocessableEntity,
)


T = TypeVar("T")
U = TypeVar("U")


class AsyncHttpResponse(HttpResponse, Protocol):
    request_info: HttpRequestP
    status: int

    async def text(self) -> str:  # type: ignore
        ...

    async def json(self, *args: Any, **kwargs: Any) -> dict[str, Any]:  # type: ignore
        ...


class AsyncResponse(Response[AsyncHttpResponse]): ...


class Session:
    __slots__ = ("credentials", "default_headers", "enable_caching", "language", "reconnect", "request_id_generator", "session", "user_agent")

    def __init__(
        self,
        credentials: UDM,
        language: str = "en-US",
        reconnect: bool = True,
        user_agent: str = "univention.lib/1.0",
        enable_caching: bool = False,
        concurrency_limit: int = 10,
        request_id_generator: Callable[[], str | None] | None = None,
    ) -> None:
        self.language = language
        self.credentials = credentials
        self.reconnect = reconnect
        self.user_agent = user_agent
        self.enable_caching = enable_caching
        self.request_id_generator = request_id_generator or (lambda: uuid.uuid4().hex)
        self.default_headers = {
            "Accept": "application/hal+json; q=1, application/json; q=0.9; text/html; q=0.2, */*; q=0.1",
            "Accept-Language": self.language,
            "User-Agent": self.user_agent,
        }
        self.session = self.create_session(concurrency_limit)

    async def __aenter__(self) -> Session:
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> None:
        await self.session.__aexit__(exc_type, exc_value, traceback)

    def create_session(self, concurrency_limit: int = 10) -> aiohttp.ClientSession:
        connector = aiohttp.TCPConnector(limit=concurrency_limit)
        auth = aiohttp.BasicAuth(self.credentials.username, self.credentials.password)  # type: ignore
        return aiohttp.ClientSession(connector=connector, auth=auth)

    def get_method(self, method: str) -> Callable[..., Awaitable[AsyncHttpResponse]]:
        sess = self.session
        func_mapping: dict[str, Callable[..., Awaitable[aiohttp.ClientResponse]]] = {
            "GET": sess.get,
            "POST": sess.post,
            "PUT": sess.put,
            "DELETE": sess.delete,
            "PATCH": sess.patch,
            "OPTIONS": sess.options,
        }
        return cast(Callable[..., Awaitable[AsyncHttpResponse]], func_mapping.get(method.upper(), sess.get))

    async def request(self, method: str, uri: str, data: dict[str, Any] | None = None, expect_json: bool = False, **headers: str | None) -> Any:
        return (await self.make_request(method, uri, data, expect_json=expect_json, **headers)).data  # type: ignore # <https://github.com/python/mypy/issues/10008>

    async def make_request(
        self,
        method: str,
        uri: str,
        data: dict[str, Any] | None = None,
        expect_json: bool = False,
        allow_redirects: bool = True,
        custom_redirect_handling: bool = False,
        **headers: str | None,
    ) -> AsyncResponse:
        if method in ("GET", "HEAD"):
            params = data
            json = None
        else:
            params = None
            json = data
        if "X-Request-Id" not in headers:
            headers["X-Request-Id"] = self.request_id_generator()

        async def doit() -> AsyncResponse:
            try:
                response: AsyncHttpResponse = await self.get_method(method)(
                    uri, params=params, json=json, headers=dict(self.default_headers, **headers), allow_redirects=allow_redirects
                )
            except aiohttp.ClientConnectionError as exc:  # pragma: no cover
                raise ConnectionError(exc) from exc
            if custom_redirect_handling:
                response = await self._follow_redirection(response)
            data = await self.eval_response(response, expect_json=expect_json)
            return AsyncResponse(response, data, uri)

        for _i in range(5):
            try:
                return await doit()
            except ServiceUnavailable as exc:  # TODO: same for ConnectionError? python-request does it itself.
                if not self.reconnect:  # pragma: no cover
                    raise
                try:
                    assert exc.response is not None
                    retry_after = min(5, int(exc.response.headers.get("Retry-After", 1)))
                except ValueError:  # pragma: no cover
                    retry_after = 1
                await asyncio.sleep(retry_after)

        return await doit()

    async def _follow_redirection(self, response: AsyncHttpResponse) -> AsyncHttpResponse:
        location = response.headers.get("Location")
        #  aiohttp doesn't follow redirects for 202?
        if location and response.status in (201, 202):
            response = (await self.make_request("GET", location, allow_redirects=False)).response

        # prevent allow_redirects because it does not wait Retry-After time causing a break up after 30 fast redirections
        while 300 <= response.status <= 399 and "Location" in response.headers:
            location = response.headers["Location"]
            if response.headers.get("Retry-After", "").isdigit():
                await asyncio.sleep(min(30, max(0, int(response.headers["Retry-After"]))))
            response = (await self.make_request(self._select_method(response), location, allow_redirects=False)).response

        return response

    def _select_method(self, response: AsyncHttpResponse) -> str:
        if response.status in (300, 301, 303) and response.request_info.method != "HEAD":
            return "GET"
        return response.request_info.method  # pragma: no cover

    async def eval_response(self, response: AsyncHttpResponse, expect_json: bool = False) -> Any:
        if response.status >= 399:
            msg = f"{response.request_info.method} {response.url}: {response.status}"
            error_details = None
            try:
                json = await response.json()
            except (ValueError, aiohttp.client_exceptions.ContentTypeError):  # pragma: no cover
                pass
            else:
                if isinstance(json, dict):
                    error_details = json.get("error", {})
                    with contextlib.suppress(NoRelation):
                        error_details["error"] = [error async for error in self.resolve_relations(json, "udm:error")]
                    if error_details:
                        server_message = error_details.get("message")
                        # traceback = error_details.get('traceback')
                        if server_message:
                            msg += f"\n{server_message}"
            errors: dict[int, type[HTTPError]] = {
                400: BadRequest,
                404: NotFound,
                403: Forbidden,
                401: Unauthorized,
                412: PreconditionFailed,
                422: UnprocessableEntity,
                500: ServerError,
                503: ServiceUnavailable,
            }
            cls = errors.get(response.status, HTTPError)
            raise cls(response.status, msg, response, error_details=error_details)
        if response.headers.get("Content-Type") in ("application/json", "application/hal+json"):
            return await response.json()
        elif expect_json:  # pragma: no cover
            raise UnexpectedResponse(await response.text())
        return await response.text()

    def get_relations(self, entry: dict[str, Any], relation: str, name: str | None = None, template: dict[str, Any] | None = None) -> Iterator[dict[str, str]]:
        links = copy.deepcopy(entry.get("_links", {}))
        links = links.get(relation, [None])
        links = links if links and isinstance(links, list) else [links]
        links = [link for link in links if isinstance(link, dict) and (not name or link.get("name") == name)]
        for link in sorted(links, key=lambda x: not x.get("templated", False) if template else x.get("templated", False)):
            if link.get("deprecation"):
                pass  # TODO: log warning
            if link.get("templated"):
                link["href"] = uritemplate.expand(link["href"], template)
            yield link

    def get_relation(self, entry: dict[str, Any], relation: str, name: str | None = None, template: dict[str, Any] | None = None) -> dict[str, str]:
        try:
            return next(self.get_relations(entry, relation, name, template))
        except StopIteration as exc:  # pragma: no cover
            raise NoRelation(relation) from exc

    async def resolve_relations(self, entry: dict[str, Any], relation: str, name: str | None = None, template: dict[str, Any] | None = None) -> AsyncIterator[dict[str, Any]]:
        embedded = entry.get("_embedded", {})
        if isinstance(embedded, dict) and relation in embedded:
            # yield from embedded[relation]
            for x in embedded[relation]:
                yield x
            return

        for rel in self.get_relations(entry, relation, name, template):
            yield (await self.make_request("GET", rel["href"])).data

    async def resolve_relation(self, entry: dict[str, Any], relation: str, name: str | None = None, template: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            return await anext(self.resolve_relations(entry, relation, name, template))
        except StopAsyncIteration as exc:  # pragma: no cover
            raise NoRelation(relation) from exc


class Client:
    __slots__ = ("client",)

    def __init__(self, client: Session) -> None:
        self.client = client


class UDM(Client):
    __slots__ = ("bearer_token", "entry", "password", "uri", "username")

    @classmethod
    def http(
        cls,
        uri: str,
        username: str,
        password: str,
        *,
        request_id_generator: Callable[[], str | None] | None = None,
    ) -> UDM:
        return cls(uri, username, password, request_id_generator=request_id_generator)

    @classmethod  # pragma: no cover
    def bearer(
        cls,
        uri: str,
        bearer_token: str,
        *,
        request_id_generator: Callable[[], str | None] | None = None,
    ) -> UDM:
        return cls(uri, None, None, bearer_token=bearer_token, request_id_generator=request_id_generator)

    def __init__(self, uri: str, username: str | None, password: str | None, *args: Any, request_id_generator: Callable[[], str | None] | None = None, **kwargs: Any) -> None:
        self.uri = uri
        self.username = username
        self.password = password
        self.bearer_token = kwargs.pop("bearer_token", None)
        self.entry: dict[str, Any] | Any | None = None
        super().__init__(Session(self, *args, request_id_generator=request_id_generator, **kwargs))  # type: ignore

    async def __aenter__(self) -> UDM:
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> None:
        await self.client.__aexit__(exc_type, exc_value, traceback)

    async def load(self) -> None:
        # FIXME: use HTTP caching instead of memory caching
        if self.entry is None:
            await self.reload()

    async def reload(self) -> None:
        self.entry = await self.client.request("GET", self.uri, expect_json=True)

    async def get_ldap_base(self) -> str | None:
        await self.load()
        assert self.entry is not None
        return Object.from_data(self, await self.client.resolve_relation(self.entry, "udm:ldap-base")).dn

    async def modules(self, name: str | None = None) -> AsyncIterator[Module]:
        await self.load()
        assert self.entry is not None
        async for module in self.client.resolve_relations(self.entry, "udm:object-modules"):
            for module_info in self.client.get_relations(module, "udm:object-types", name):
                yield Module(self, module_info["href"], module_info["name"], module_info["title"])

    async def obj_by_dn(self, dn: str) -> Object:
        await self.load()
        assert self.entry is not None
        return Object.from_data(self, await self.client.resolve_relation(self.entry, "udm:object/get-by-dn", template={"dn": dn}))

    async def obj_by_uuid(self, uuid: str) -> Object:
        await self.load()
        assert self.entry is not None
        return Object.from_data(self, await self.client.resolve_relation(self.entry, "udm:object/get-by-uuid", template={"uuid": uuid}))

    async def get(self, name: str) -> Module | None:
        async for module in self.modules(name):
            return module

        return None

    async def get_object(self, object_type: str, dn: str) -> Object | None:
        mod = await self.get(object_type)
        assert mod
        obj = await mod.get(dn)
        return obj

    def __repr__(self) -> str:
        return f"UDM(uri={self.uri!r}, username={self.username!r}, password=***)"


class Module(Client):
    __slots__ = ("name", "password", "relations", "title", "udm", "uri", "username")

    def __init__(self, udm: UDM, uri: str, name: str, title: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(udm.client, *args, **kwargs)
        self.udm = udm
        self.uri = uri
        self.username = udm.username
        self.password = udm.password
        self.name = name
        self.title = title
        self.relations: dict[str, Any] = {}

    async def load_relations(self) -> None:
        if self.relations:
            return
        self.relations = await self.client.request("GET", self.uri)

    def __repr__(self) -> str:
        return f"Module(uri={self.uri!r}, name={self.name!r})"

    async def new(self, position: str | None = None, superordinate: str | None = None, template: dict[str, Any] | None = None) -> Object:
        await self.load_relations()
        data = {"position": position, "superordinate": superordinate, "template": template}
        resp = await self.client.resolve_relation(self.relations, "create-form", template=data)
        return Object.from_data(self.udm, resp)

    async def get(self, dn: str, properties: list[str] | None = None) -> Object:
        # TODO: use a link relation instead of a search
        async for obj in self._search_closed(position=dn, scope="base", properties=properties):
            return await obj.open()
        raise NotFound(404, "Wrong object type!?", None)  # FIXME: object exists but is of different module. should be fixed on the server.

    async def get_by_entry_uuid(self, uuid: str, properties: list[str] | None = None) -> Object:
        # TODO: use a link relation instead of a search
        # return self.udm.get_by_uuid(uuid)
        async for obj in self._search_closed(filter={"entryUUID": uuid}, scope="base", properties=properties):
            return await obj.open()
        raise NotFound(404, "Wrong object type!?", None)  # FIXME: object exists but is of different module. should be fixed on the server.

    async def get_by_id(self, id_: str, properties: list[str] | None = None) -> Object:  # pragma: no cover
        # TODO: Needed?
        raise NotImplementedError()

    async def search(
        self,
        filter: dict[str, str] | str | bytes | None = None,
        position: str | None = None,
        scope: str | None = "sub",
        hidden: bool = False,
        superordinate: str | None = None,
        opened: bool = False,
        properties: list[str] | None = None,
    ) -> AsyncIterator[Object | AsyncShallowObject]:
        if opened:
            async for obj in cast(AsyncIterator[Object], aiter(self._search_opened(filter, position, scope, hidden, superordinate, properties))):
                yield obj
        else:
            async for shallow_obj in cast(AsyncIterator[AsyncShallowObject], aiter(self._search_closed(filter, position, scope, hidden, superordinate, properties))):
                yield shallow_obj

    async def _search_opened(
        self,
        filter: dict[str, str] | str | bytes | None = None,
        position: str | None = None,
        scope: str | None = "sub",
        hidden: bool = False,
        superordinate: str | None = None,
        properties: list[str] | None = None,
    ) -> AsyncIterator[Object]:
        async for obj in self._search(filter, position, scope, hidden, superordinate, True, properties):
            yield Object.from_data(self.udm, obj)  # NOTE: this is missing last-modified, therefore no conditional request is done on modification!

    async def _search_closed(
        self,
        filter: dict[str, str] | str | bytes | None = None,
        position: str | None = None,
        scope: str | None = "sub",
        hidden: bool = False,
        superordinate: str | None = None,
        properties: list[str] | None = None,
    ) -> AsyncIterator[AsyncShallowObject]:
        async for obj in self._search(filter, position, scope, hidden, superordinate, False, properties):
            objself = self.client.get_relation(obj, "self")
            uri = objself["href"]
            dn = objself["name"]
            yield AsyncShallowObject(self.udm, dn, uri)

    async def _search(
        self,
        filter: dict[str, str] | str | bytes | None = None,
        position: str | None = None,
        scope: str | None = "sub",
        hidden: bool = False,
        superordinate: str | None = None,
        opened: bool = False,
        properties: list[str] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        data: dict[str, str | list[str] | dict[str, Any] | None] = {
            "position": position,
            "scope": scope,
            "hidden": "1" if hidden else "0",
        }
        if isinstance(filter, dict):
            for prop, val in filter.items():
                data.setdefault("query", {})[f"query[{prop}]"] = val  # type: ignore
        elif isinstance(filter, str):
            data["filter"] = filter
        if superordinate:
            data["superordinate"] = superordinate
        if not opened:
            data["opened"] = "0"
            data["properties"] = ["dn"]
        if properties:
            data["properties"] = properties
        await self.load_relations()
        entries = await self.client.resolve_relation(self.relations, "search", template=data)
        async for entry in self.client.resolve_relations(entries, "udm:object"):
            yield entry

    async def get_layout(self) -> Any | None:
        await self.load_relations()
        relation = await self.udm.client.resolve_relation(self.relations, "udm:layout")
        return relation.get("layout")

    async def get_properties(self) -> Any | None:
        await self.load_relations()
        return (await self.udm.client.resolve_relation(self.relations, "udm:properties")).get("properties")

    async def get_property_choices(self, property: str) -> Any | None:
        await self.load_relations()
        relations = await self.udm.client.resolve_relation(self.relations, "udm:properties")
        return (await self.udm.client.resolve_relation(relations, "udm:property-choices", name=property)).get("choices")

    async def policy_result(self, policy_module: str, position: str, policy: str | None = None) -> dict[str, Any]:
        await self.load_relations()
        policy_result = await self.udm.client.resolve_relation(self.relations, "udm:policy-result", name=policy_module, template={"position": position, "policy": policy})
        policy_result.pop("_links", None)
        policy_result.pop("_embedded", None)
        return policy_result

    async def get_report_types(self) -> list[str]:
        await self.load_relations()
        return [x["name"] for x in self.udm.client.get_relations(self.relations, "udm:report", template={"dn": ""}) if x.get("name")]

    async def create_report(self, report_type: str, object_dns: list[str]) -> Any:
        await self.load_relations()
        return await self.udm.client.resolve_relation(self.relations, "udm:report", name=report_type, template={"dn": object_dns})


class AsyncShallowObject(Client):
    __slots__ = ("dn", "udm", "uri")

    def __init__(self, udm: UDM, dn: str | None, uri: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(udm.client, *args, **kwargs)
        self.dn = dn
        self.udm = udm
        self.uri = uri

    async def open(self) -> Object:
        return Object.from_response(self.udm, await self.client.make_request("GET", self.uri))

    def __repr__(self) -> str:
        return f"AsyncShallowObject(dn={self.dn!r})"


class AsyncReferences(SyncReferences):
    shallow_object_class: type[Any] = AsyncShallowObject


class Object(ObjectRepr, Client):
    __slots__ = tuple(["etag", "hal", "last_modified", "representation"] + list(Client.__slots__))

    objects = AsyncReferences()

    def __init__(self, udm: UDM, representation: dict[str, Any], etag: str | None = None, last_modified: str | None = None, *args: Any, **kwargs: Any) -> None:
        Client.__init__(self, udm.client, *args, **kwargs)
        ObjectRepr.__init__(self, representation, etag, last_modified)
        self.udm = udm

    def _copy_from_obj(self, obj: ObjectCopyProto) -> None:
        ObjectRepr._copy_from_obj(self, obj)
        self.udm = obj.udm

    @property
    def module(self) -> Awaitable[Module | None]:
        # FIXME: use "type" relation link
        # object_type = self.udm.get_relation(self.hal, 'type')['href']
        return self.udm.get(self.object_type)

    @property
    def uri(self) -> str | None:
        try:
            uri = self.client.get_relation(self.hal, "self")
        except NoRelation:
            uri = None
        if uri:
            return uri["href"]
        return self.representation.get("uri")

    @classmethod
    def from_response(cls, udm: UDM, response: AsyncResponse) -> Object:
        return cls.from_data(udm, response.data, response.response.headers)

    @classmethod
    def from_data(cls, udm: UDM, entry: dict[str, Any], headers: Mapping[str, str] | None = None) -> Object:
        headers = headers or {}
        return cls(udm, entry, etag=headers.get("Etag"), last_modified=headers.get("Last-Modified"))

    def __repr__(self) -> str:
        return f"Object(module={self.object_type!r}, dn={self.dn!r}, uri={self.uri!r})"

    async def reload(self) -> None:
        try:
            uri = self.client.get_relation(self.hal, "self")
        except NoRelation:
            uri = None
        if uri:
            obj = await AsyncShallowObject(self.udm, self.dn, uri["href"]).open()
        else:
            module = await self.module
            assert module and self.dn
            obj = await module.get(self.dn)
        self._copy_from_obj(obj)

    async def save(self, reload: bool = True) -> AsyncResponse:
        if self.dn:
            return await self._modify(reload)
        else:
            return await self._create(reload)

    async def json_patch(self, patch: dict[str, Any], reload: bool = True) -> AsyncResponse:
        if self.dn:
            return await self._patch(patch, reload=reload)
        else:
            uri = self.client.get_relation(self.hal, "create")
            return await self._request("POST", uri["href"], patch, {"Content-Type": "application/json-patch+json"})

    async def delete(self, remove_referring: bool = False) -> bytes:
        assert self.uri
        headers = {
            key: value
            for key, value in {
                "If-Unmodified-Since": self.last_modified,
                "If-Match": self.etag,
            }.items()
            if value
        }
        return await self.client.request("DELETE", self.uri, **headers)  # type: ignore # <https://github.com/python/mypy/issues/10008>

    async def move(self, position: str, reload: bool = True) -> None:
        self.position = position
        await self.save(reload=reload)

    async def _modify(self, reload: bool = True) -> AsyncResponse:
        assert self.uri
        headers = {
            key: value
            for key, value in {
                "If-Unmodified-Since": self.last_modified,
                "If-Match": self.etag,
            }.items()
            if value
        }
        return await self._request("PUT", self.uri, self.representation, headers, reload=reload)

    async def _patch(self, data: dict[str, Any], reload: bool = True) -> AsyncResponse:
        assert self.uri
        headers = {
            key: value
            for key, value in {
                "If-Unmodified-Since": self.last_modified,
                "If-Match": self.etag,
                "Content-Type": "application/json-patch+json",
            }.items()
            if value
        }
        return await self._request("PATCH", self.uri, data, headers, reload=reload)

    async def _create(self, reload: bool = True) -> AsyncResponse:
        uri = self.client.get_relation(self.hal, "create")
        return await self._request("POST", uri["href"], self.representation, {}, reload=reload)

    async def _request(self, method: str, uri: str, data: dict[str, Any], headers: dict[str, Any], reload: bool = True) -> AsyncResponse:
        response = await self.client.make_request(method, uri, data=data, allow_redirects=False, custom_redirect_handling=True, **headers)
        await self._reload_from_response(response, reload)
        return response

    async def _reload_from_response(self, response: AsyncResponse, reload: bool) -> None:
        if reload and 200 <= response.response.status <= 299 and "Location" in response.response.headers:
            uri = response.response.headers["Location"]
            obj = AsyncShallowObject(self.udm, None, uri)
            self._copy_from_obj(await obj.open())
            return

        if response.response.status == 200:
            # the response already contains a new representation
            self._copy_from_obj(Object.from_response(self.udm, response))
            return

        if reload:  # pragma: no cover
            await self.reload()

    async def generate_service_specific_password(self, service: str) -> Any | None:
        uri = self.client.get_relation(self.hal, "udm:service-specific-password")["href"]
        response = await self.client.make_request("POST", uri, data={"service": service})
        return response.data.get("password", None)

    async def get_layout(self) -> Any | None:
        return (await self.udm.client.resolve_relation(self.hal, "udm:layout")).get("layout")

    async def get_properties(self) -> Any | None:
        return (await self.udm.client.resolve_relation(self.hal, "udm:properties")).get("properties")

    async def get_property_choices(self, property: str) -> Any | None:
        hal = await self.udm.client.resolve_relation(self.hal, "udm:properties")
        return (await self.udm.client.resolve_relation(hal, "udm:property-choices", name=property)).get("choices")

    async def policy_result(self, policy_module: str, policy: str | None = None) -> dict[str, Any]:
        policy_result = await self.udm.client.resolve_relation(self.hal, "udm:policy-result", name=policy_module, template={"policy": policy})
        policy_result.pop("_links", None)
        policy_result.pop("_embedded", None)
        return policy_result
