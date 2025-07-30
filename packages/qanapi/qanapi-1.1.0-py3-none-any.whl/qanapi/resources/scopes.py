# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import scope_create_params, scope_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.scope_list_response import ScopeListResponse
from ..types.scope_create_response import ScopeCreateResponse
from ..types.scope_delete_response import ScopeDeleteResponse
from ..types.scope_update_response import ScopeUpdateResponse
from ..types.scope_retrieve_response import ScopeRetrieveResponse

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

    def create(
        self,
        *,
        name: str,
        route: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeCreateResponse:
        """
        Create a new scope

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/scopes",
            body=maybe_transform(
                {
                    "name": name,
                    "route": route,
                },
                scope_create_params.ScopeCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeCreateResponse,
        )

    def retrieve(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeRetrieveResponse:
        """
        Get a specific scope

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/scopes/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeRetrieveResponse,
        )

    def update(
        self,
        id: int,
        *,
        name: str | NotGiven = NOT_GIVEN,
        route: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeUpdateResponse:
        """
        Update a scope

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            f"/scopes/{id}",
            body=maybe_transform(
                {
                    "name": name,
                    "route": route,
                },
                scope_update_params.ScopeUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeUpdateResponse,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeListResponse:
        """List all scopes"""
        return self._get(
            "/scopes",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeListResponse,
        )

    def delete(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeDeleteResponse:
        """
        Delete a scope

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._delete(
            f"/scopes/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeDeleteResponse,
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

    async def create(
        self,
        *,
        name: str,
        route: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeCreateResponse:
        """
        Create a new scope

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/scopes",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "route": route,
                },
                scope_create_params.ScopeCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeCreateResponse,
        )

    async def retrieve(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeRetrieveResponse:
        """
        Get a specific scope

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/scopes/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeRetrieveResponse,
        )

    async def update(
        self,
        id: int,
        *,
        name: str | NotGiven = NOT_GIVEN,
        route: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeUpdateResponse:
        """
        Update a scope

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            f"/scopes/{id}",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "route": route,
                },
                scope_update_params.ScopeUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeUpdateResponse,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeListResponse:
        """List all scopes"""
        return await self._get(
            "/scopes",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeListResponse,
        )

    async def delete(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScopeDeleteResponse:
        """
        Delete a scope

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._delete(
            f"/scopes/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScopeDeleteResponse,
        )


class ScopesResourceWithRawResponse:
    def __init__(self, scopes: ScopesResource) -> None:
        self._scopes = scopes

        self.create = to_raw_response_wrapper(
            scopes.create,
        )
        self.retrieve = to_raw_response_wrapper(
            scopes.retrieve,
        )
        self.update = to_raw_response_wrapper(
            scopes.update,
        )
        self.list = to_raw_response_wrapper(
            scopes.list,
        )
        self.delete = to_raw_response_wrapper(
            scopes.delete,
        )


class AsyncScopesResourceWithRawResponse:
    def __init__(self, scopes: AsyncScopesResource) -> None:
        self._scopes = scopes

        self.create = async_to_raw_response_wrapper(
            scopes.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            scopes.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            scopes.update,
        )
        self.list = async_to_raw_response_wrapper(
            scopes.list,
        )
        self.delete = async_to_raw_response_wrapper(
            scopes.delete,
        )


class ScopesResourceWithStreamingResponse:
    def __init__(self, scopes: ScopesResource) -> None:
        self._scopes = scopes

        self.create = to_streamed_response_wrapper(
            scopes.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            scopes.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            scopes.update,
        )
        self.list = to_streamed_response_wrapper(
            scopes.list,
        )
        self.delete = to_streamed_response_wrapper(
            scopes.delete,
        )


class AsyncScopesResourceWithStreamingResponse:
    def __init__(self, scopes: AsyncScopesResource) -> None:
        self._scopes = scopes

        self.create = async_to_streamed_response_wrapper(
            scopes.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            scopes.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            scopes.update,
        )
        self.list = async_to_streamed_response_wrapper(
            scopes.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            scopes.delete,
        )
