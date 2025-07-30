# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import auth, scopes, decrypt, encrypt
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import QanapiError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.api_keys import api_keys

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Qanapi", "AsyncQanapi", "Client", "AsyncClient"]


class Qanapi(SyncAPIClient):
    auth: auth.AuthResource
    encrypt: encrypt.EncryptResource
    decrypt: decrypt.DecryptResource
    api_keys: api_keys.APIKeysResource
    scopes: scopes.ScopesResource
    with_raw_response: QanapiWithRawResponse
    with_streaming_response: QanapiWithStreamedResponse

    # client options
    api_key: str
    subdomain: str
    bearer_token: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        subdomain: str | None = None,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Qanapi client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `QANAPI_API_KEY`
        - `subdomain` from `QANAPI_SUBDOMAIN`
        """
        if api_key is None:
            api_key = os.environ.get("QANAPI_API_KEY")
        if api_key is None:
            raise QanapiError(
                "The api_key client option must be set either by passing api_key to the client or by setting the QANAPI_API_KEY environment variable"
            )
        self.api_key = api_key

        if subdomain is None:
            subdomain = os.environ.get("QANAPI_SUBDOMAIN")
        if subdomain is None:
            raise QanapiError(
                "The subdomain client option must be set either by passing subdomain to the client or by setting the QANAPI_SUBDOMAIN environment variable"
            )
        self.subdomain = subdomain

        self.bearer_token = bearer_token

        if base_url is None:
            base_url = os.environ.get("QANAPI_BASE_URL")
        if base_url is None:
            base_url = f"https://{subdomain}.qanapi.cloud/api/v2"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.auth = auth.AuthResource(self)
        self.encrypt = encrypt.EncryptResource(self)
        self.decrypt = decrypt.DecryptResource(self)
        self.api_keys = api_keys.APIKeysResource(self)
        self.scopes = scopes.ScopesResource(self)
        self.with_raw_response = QanapiWithRawResponse(self)
        self.with_streaming_response = QanapiWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._api_key_auth, **self._bearer_auth}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-qanapi-authorization": api_key}

    @property
    def _bearer_auth(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        if bearer_token is None:
            return {}
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        subdomain: str | None = None,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            subdomain=subdomain or self.subdomain,
            bearer_token=bearer_token or self.bearer_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncQanapi(AsyncAPIClient):
    auth: auth.AsyncAuthResource
    encrypt: encrypt.AsyncEncryptResource
    decrypt: decrypt.AsyncDecryptResource
    api_keys: api_keys.AsyncAPIKeysResource
    scopes: scopes.AsyncScopesResource
    with_raw_response: AsyncQanapiWithRawResponse
    with_streaming_response: AsyncQanapiWithStreamedResponse

    # client options
    api_key: str
    subdomain: str
    bearer_token: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        subdomain: str | None = None,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncQanapi client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `QANAPI_API_KEY`
        - `subdomain` from `QANAPI_SUBDOMAIN`
        """
        if api_key is None:
            api_key = os.environ.get("QANAPI_API_KEY")
        if api_key is None:
            raise QanapiError(
                "The api_key client option must be set either by passing api_key to the client or by setting the QANAPI_API_KEY environment variable"
            )
        self.api_key = api_key

        if subdomain is None:
            subdomain = os.environ.get("QANAPI_SUBDOMAIN")
        if subdomain is None:
            raise QanapiError(
                "The subdomain client option must be set either by passing subdomain to the client or by setting the QANAPI_SUBDOMAIN environment variable"
            )
        self.subdomain = subdomain

        self.bearer_token = bearer_token

        if base_url is None:
            base_url = os.environ.get("QANAPI_BASE_URL")
        if base_url is None:
            base_url = f"https://{subdomain}.qanapi.cloud/api/v2"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.auth = auth.AsyncAuthResource(self)
        self.encrypt = encrypt.AsyncEncryptResource(self)
        self.decrypt = decrypt.AsyncDecryptResource(self)
        self.api_keys = api_keys.AsyncAPIKeysResource(self)
        self.scopes = scopes.AsyncScopesResource(self)
        self.with_raw_response = AsyncQanapiWithRawResponse(self)
        self.with_streaming_response = AsyncQanapiWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._api_key_auth, **self._bearer_auth}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-qanapi-authorization": api_key}

    @property
    def _bearer_auth(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        if bearer_token is None:
            return {}
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        subdomain: str | None = None,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            subdomain=subdomain or self.subdomain,
            bearer_token=bearer_token or self.bearer_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class QanapiWithRawResponse:
    def __init__(self, client: Qanapi) -> None:
        self.auth = auth.AuthResourceWithRawResponse(client.auth)
        self.encrypt = encrypt.EncryptResourceWithRawResponse(client.encrypt)
        self.decrypt = decrypt.DecryptResourceWithRawResponse(client.decrypt)
        self.api_keys = api_keys.APIKeysResourceWithRawResponse(client.api_keys)
        self.scopes = scopes.ScopesResourceWithRawResponse(client.scopes)


class AsyncQanapiWithRawResponse:
    def __init__(self, client: AsyncQanapi) -> None:
        self.auth = auth.AsyncAuthResourceWithRawResponse(client.auth)
        self.encrypt = encrypt.AsyncEncryptResourceWithRawResponse(client.encrypt)
        self.decrypt = decrypt.AsyncDecryptResourceWithRawResponse(client.decrypt)
        self.api_keys = api_keys.AsyncAPIKeysResourceWithRawResponse(client.api_keys)
        self.scopes = scopes.AsyncScopesResourceWithRawResponse(client.scopes)


class QanapiWithStreamedResponse:
    def __init__(self, client: Qanapi) -> None:
        self.auth = auth.AuthResourceWithStreamingResponse(client.auth)
        self.encrypt = encrypt.EncryptResourceWithStreamingResponse(client.encrypt)
        self.decrypt = decrypt.DecryptResourceWithStreamingResponse(client.decrypt)
        self.api_keys = api_keys.APIKeysResourceWithStreamingResponse(client.api_keys)
        self.scopes = scopes.ScopesResourceWithStreamingResponse(client.scopes)


class AsyncQanapiWithStreamedResponse:
    def __init__(self, client: AsyncQanapi) -> None:
        self.auth = auth.AsyncAuthResourceWithStreamingResponse(client.auth)
        self.encrypt = encrypt.AsyncEncryptResourceWithStreamingResponse(client.encrypt)
        self.decrypt = decrypt.AsyncDecryptResourceWithStreamingResponse(client.decrypt)
        self.api_keys = api_keys.AsyncAPIKeysResourceWithStreamingResponse(client.api_keys)
        self.scopes = scopes.AsyncScopesResourceWithStreamingResponse(client.scopes)


Client = Qanapi

AsyncClient = AsyncQanapi
