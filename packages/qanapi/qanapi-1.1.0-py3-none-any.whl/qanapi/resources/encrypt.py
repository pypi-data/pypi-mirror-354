# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, List, Union, Iterable, cast

import httpx

from ..types import encrypt_encrypt_data_params
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
from ..types.encrypt_encrypt_data_response import EncryptEncryptDataResponse

__all__ = ["EncryptResource", "AsyncEncryptResource"]


class EncryptResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EncryptResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#accessing-raw-response-data-eg-headers
        """
        return EncryptResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EncryptResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#with_streaming_response
        """
        return EncryptResourceWithStreamingResponse(self)

    def encrypt_data(
        self,
        *,
        data: Union[str, float, Dict[str, object], Iterable[object]],
        access: encrypt_encrypt_data_params.Access | NotGiven = NOT_GIVEN,
        attributes: encrypt_encrypt_data_params.Attributes | NotGiven = NOT_GIVEN,
        sensitive_fields: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EncryptEncryptDataResponse:
        """
        Encrypt data with optional ACL

        Args:
          data: The actual data to encrypt.

              - Can be a scalar (string/number), object, or array.
              - If the value is an object or array, only the specified `sensitiveFields` are
                encrypted.

          attributes: Optional metadata describing the data's context.

          sensitive_fields: Laravel-style dot-notated paths to fields that should be encrypted.

              Supports:

              - Dot notation for nested fields: `user.profile.ssn`
              - Wildcard `*` for arrays or dynamic keys: `users.*.token`

              Examples:

              - `password`
              - `user.credentials.secret`
              - `accounts.*.secret`
              - `teams.*.members.*.email`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            EncryptEncryptDataResponse,
            self._post(
                "/encrypt",
                body=maybe_transform(
                    {
                        "data": data,
                        "access": access,
                        "attributes": attributes,
                        "sensitive_fields": sensitive_fields,
                    },
                    encrypt_encrypt_data_params.EncryptEncryptDataParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, EncryptEncryptDataResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncEncryptResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEncryptResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEncryptResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEncryptResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#with_streaming_response
        """
        return AsyncEncryptResourceWithStreamingResponse(self)

    async def encrypt_data(
        self,
        *,
        data: Union[str, float, Dict[str, object], Iterable[object]],
        access: encrypt_encrypt_data_params.Access | NotGiven = NOT_GIVEN,
        attributes: encrypt_encrypt_data_params.Attributes | NotGiven = NOT_GIVEN,
        sensitive_fields: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EncryptEncryptDataResponse:
        """
        Encrypt data with optional ACL

        Args:
          data: The actual data to encrypt.

              - Can be a scalar (string/number), object, or array.
              - If the value is an object or array, only the specified `sensitiveFields` are
                encrypted.

          attributes: Optional metadata describing the data's context.

          sensitive_fields: Laravel-style dot-notated paths to fields that should be encrypted.

              Supports:

              - Dot notation for nested fields: `user.profile.ssn`
              - Wildcard `*` for arrays or dynamic keys: `users.*.token`

              Examples:

              - `password`
              - `user.credentials.secret`
              - `accounts.*.secret`
              - `teams.*.members.*.email`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            EncryptEncryptDataResponse,
            await self._post(
                "/encrypt",
                body=await async_maybe_transform(
                    {
                        "data": data,
                        "access": access,
                        "attributes": attributes,
                        "sensitive_fields": sensitive_fields,
                    },
                    encrypt_encrypt_data_params.EncryptEncryptDataParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, EncryptEncryptDataResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class EncryptResourceWithRawResponse:
    def __init__(self, encrypt: EncryptResource) -> None:
        self._encrypt = encrypt

        self.encrypt_data = to_raw_response_wrapper(
            encrypt.encrypt_data,
        )


class AsyncEncryptResourceWithRawResponse:
    def __init__(self, encrypt: AsyncEncryptResource) -> None:
        self._encrypt = encrypt

        self.encrypt_data = async_to_raw_response_wrapper(
            encrypt.encrypt_data,
        )


class EncryptResourceWithStreamingResponse:
    def __init__(self, encrypt: EncryptResource) -> None:
        self._encrypt = encrypt

        self.encrypt_data = to_streamed_response_wrapper(
            encrypt.encrypt_data,
        )


class AsyncEncryptResourceWithStreamingResponse:
    def __init__(self, encrypt: AsyncEncryptResource) -> None:
        self._encrypt = encrypt

        self.encrypt_data = async_to_streamed_response_wrapper(
            encrypt.encrypt_data,
        )
