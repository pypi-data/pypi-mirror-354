# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .scopes import (
    ScopesResource,
    AsyncScopesResource,
    ScopesResourceWithRawResponse,
    AsyncScopesResourceWithRawResponse,
    ScopesResourceWithStreamingResponse,
    AsyncScopesResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.api_key_revoke_response import APIKeyRevokeResponse
from ...types.api_key_rotate_response import APIKeyRotateResponse

__all__ = ["APIKeysResource", "AsyncAPIKeysResource"]


class APIKeysResource(SyncAPIResource):
    @cached_property
    def scopes(self) -> ScopesResource:
        return ScopesResource(self._client)

    @cached_property
    def with_raw_response(self) -> APIKeysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#accessing-raw-response-data-eg-headers
        """
        return APIKeysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> APIKeysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#with_streaming_response
        """
        return APIKeysResourceWithStreamingResponse(self)

    def revoke(
        self,
        api_key: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIKeyRevokeResponse:
        """
        Revoke an API Key

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key:
            raise ValueError(f"Expected a non-empty value for `api_key` but received {api_key!r}")
        return self._patch(
            f"/api-keys/{api_key}/revoke",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIKeyRevokeResponse,
        )

    def rotate(
        self,
        api_key: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIKeyRotateResponse:
        """
        Rotate an API Key

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key:
            raise ValueError(f"Expected a non-empty value for `api_key` but received {api_key!r}")
        return self._patch(
            f"/api-keys/{api_key}/rotate",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIKeyRotateResponse,
        )


class AsyncAPIKeysResource(AsyncAPIResource):
    @cached_property
    def scopes(self) -> AsyncScopesResource:
        return AsyncScopesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAPIKeysResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAPIKeysResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAPIKeysResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#with_streaming_response
        """
        return AsyncAPIKeysResourceWithStreamingResponse(self)

    async def revoke(
        self,
        api_key: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIKeyRevokeResponse:
        """
        Revoke an API Key

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key:
            raise ValueError(f"Expected a non-empty value for `api_key` but received {api_key!r}")
        return await self._patch(
            f"/api-keys/{api_key}/revoke",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIKeyRevokeResponse,
        )

    async def rotate(
        self,
        api_key: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIKeyRotateResponse:
        """
        Rotate an API Key

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key:
            raise ValueError(f"Expected a non-empty value for `api_key` but received {api_key!r}")
        return await self._patch(
            f"/api-keys/{api_key}/rotate",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIKeyRotateResponse,
        )


class APIKeysResourceWithRawResponse:
    def __init__(self, api_keys: APIKeysResource) -> None:
        self._api_keys = api_keys

        self.revoke = to_raw_response_wrapper(
            api_keys.revoke,
        )
        self.rotate = to_raw_response_wrapper(
            api_keys.rotate,
        )

    @cached_property
    def scopes(self) -> ScopesResourceWithRawResponse:
        return ScopesResourceWithRawResponse(self._api_keys.scopes)


class AsyncAPIKeysResourceWithRawResponse:
    def __init__(self, api_keys: AsyncAPIKeysResource) -> None:
        self._api_keys = api_keys

        self.revoke = async_to_raw_response_wrapper(
            api_keys.revoke,
        )
        self.rotate = async_to_raw_response_wrapper(
            api_keys.rotate,
        )

    @cached_property
    def scopes(self) -> AsyncScopesResourceWithRawResponse:
        return AsyncScopesResourceWithRawResponse(self._api_keys.scopes)


class APIKeysResourceWithStreamingResponse:
    def __init__(self, api_keys: APIKeysResource) -> None:
        self._api_keys = api_keys

        self.revoke = to_streamed_response_wrapper(
            api_keys.revoke,
        )
        self.rotate = to_streamed_response_wrapper(
            api_keys.rotate,
        )

    @cached_property
    def scopes(self) -> ScopesResourceWithStreamingResponse:
        return ScopesResourceWithStreamingResponse(self._api_keys.scopes)


class AsyncAPIKeysResourceWithStreamingResponse:
    def __init__(self, api_keys: AsyncAPIKeysResource) -> None:
        self._api_keys = api_keys

        self.revoke = async_to_streamed_response_wrapper(
            api_keys.revoke,
        )
        self.rotate = async_to_streamed_response_wrapper(
            api_keys.rotate,
        )

    @cached_property
    def scopes(self) -> AsyncScopesResourceWithStreamingResponse:
        return AsyncScopesResourceWithStreamingResponse(self._api_keys.scopes)
