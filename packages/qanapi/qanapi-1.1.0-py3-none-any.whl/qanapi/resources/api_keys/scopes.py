# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.api_keys import scope_sync_params, scope_attach_params, scope_detach_params
from ...types.api_keys.scope_sync_response import ScopeSyncResponse
from ...types.api_keys.scope_attach_response import ScopeAttachResponse
from ...types.api_keys.scope_detach_response import ScopeDetachResponse
from ...types.api_keys.scope_retrieve_response import ScopeRetrieveResponse

__all__ = ["ScopesResource", "AsyncScopesResource"]


class ScopesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ScopesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ScopesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ScopesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#with_streaming_response
        """
        return ScopesResourceWithStreamingResponse(self)

    def retrieve(
        self,
        api_key: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeRetrieveResponse:
        """
        Retrieve scopes associated with an API Key

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/api-keys/{api_key}/scopes",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeRetrieveResponse,
        )

    def attach(
        self,
        api_key: int,
        *,
        scope_ids: Iterable[int],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeAttachResponse:
        """
        Attach scopes to an API Key

        Args:
          scope_ids: List of scope IDs to attach

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/api-keys/{api_key}/scopes/attach",
            body=maybe_transform({"scope_ids": scope_ids}, scope_attach_params.ScopeAttachParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeAttachResponse,
        )

    def detach(
        self,
        api_key: int,
        *,
        scope_ids: Iterable[int],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeDetachResponse:
        """
        Detach scopes from an API Key

        Args:
          scope_ids: List of scope IDs to detach

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/api-keys/{api_key}/scopes/detach",
            body=maybe_transform({"scope_ids": scope_ids}, scope_detach_params.ScopeDetachParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeDetachResponse,
        )

    def sync(
        self,
        api_key: int,
        *,
        scope_ids: Iterable[int],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeSyncResponse:
        """
        Sync scopes of an API Key

        Args:
          scope_ids: List of scope IDs to sync

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/api-keys/{api_key}/scopes/sync",
            body=maybe_transform({"scope_ids": scope_ids}, scope_sync_params.ScopeSyncParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeSyncResponse,
        )


class AsyncScopesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncScopesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncScopesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncScopesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#with_streaming_response
        """
        return AsyncScopesResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        api_key: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeRetrieveResponse:
        """
        Retrieve scopes associated with an API Key

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/api-keys/{api_key}/scopes",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeRetrieveResponse,
        )

    async def attach(
        self,
        api_key: int,
        *,
        scope_ids: Iterable[int],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeAttachResponse:
        """
        Attach scopes to an API Key

        Args:
          scope_ids: List of scope IDs to attach

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/api-keys/{api_key}/scopes/attach",
            body=await async_maybe_transform({"scope_ids": scope_ids}, scope_attach_params.ScopeAttachParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeAttachResponse,
        )

    async def detach(
        self,
        api_key: int,
        *,
        scope_ids: Iterable[int],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeDetachResponse:
        """
        Detach scopes from an API Key

        Args:
          scope_ids: List of scope IDs to detach

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/api-keys/{api_key}/scopes/detach",
            body=await async_maybe_transform({"scope_ids": scope_ids}, scope_detach_params.ScopeDetachParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeDetachResponse,
        )

    async def sync(
        self,
        api_key: int,
        *,
        scope_ids: Iterable[int],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeSyncResponse:
        """
        Sync scopes of an API Key

        Args:
          scope_ids: List of scope IDs to sync

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/api-keys/{api_key}/scopes/sync",
            body=await async_maybe_transform({"scope_ids": scope_ids}, scope_sync_params.ScopeSyncParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeSyncResponse,
        )


class ScopesResourceWithRawResponse:
    def __init__(self, scopes: ScopesResource) -> None:
        self._scopes = scopes

        self.retrieve = to_raw_response_wrapper(
            scopes.retrieve,
        )
        self.attach = to_raw_response_wrapper(
            scopes.attach,
        )
        self.detach = to_raw_response_wrapper(
            scopes.detach,
        )
        self.sync = to_raw_response_wrapper(
            scopes.sync,
        )


class AsyncScopesResourceWithRawResponse:
    def __init__(self, scopes: AsyncScopesResource) -> None:
        self._scopes = scopes

        self.retrieve = async_to_raw_response_wrapper(
            scopes.retrieve,
        )
        self.attach = async_to_raw_response_wrapper(
            scopes.attach,
        )
        self.detach = async_to_raw_response_wrapper(
            scopes.detach,
        )
        self.sync = async_to_raw_response_wrapper(
            scopes.sync,
        )


class ScopesResourceWithStreamingResponse:
    def __init__(self, scopes: ScopesResource) -> None:
        self._scopes = scopes

        self.retrieve = to_streamed_response_wrapper(
            scopes.retrieve,
        )
        self.attach = to_streamed_response_wrapper(
            scopes.attach,
        )
        self.detach = to_streamed_response_wrapper(
            scopes.detach,
        )
        self.sync = to_streamed_response_wrapper(
            scopes.sync,
        )


class AsyncScopesResourceWithStreamingResponse:
    def __init__(self, scopes: AsyncScopesResource) -> None:
        self._scopes = scopes

        self.retrieve = async_to_streamed_response_wrapper(
            scopes.retrieve,
        )
        self.attach = async_to_streamed_response_wrapper(
            scopes.attach,
        )
        self.detach = async_to_streamed_response_wrapper(
            scopes.detach,
        )
        self.sync = async_to_streamed_response_wrapper(
            scopes.sync,
        )
