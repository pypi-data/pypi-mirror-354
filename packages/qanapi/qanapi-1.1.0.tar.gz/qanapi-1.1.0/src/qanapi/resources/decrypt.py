# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, List, Union, Iterable, cast

import httpx

from ..types import decrypt_decrypt_payload_params
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
from ..types.decrypt_decrypt_payload_response import DecryptDecryptPayloadResponse

__all__ = ["DecryptResource", "AsyncDecryptResource"]


class DecryptResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DecryptResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DecryptResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DecryptResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#with_streaming_response
        """
        return DecryptResourceWithStreamingResponse(self)

    def decrypt_payload(
        self,
        *,
        data: Union[str, Dict[str, object], Iterable[object]],
        sensitive_fields: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DecryptDecryptPayloadResponse:
        """
        Decrypt encrypted payload

        Args:
          data: The encrypted payload to decrypt.

              - Can be a string or an object/array with encrypted fields.
              - Decryption is selective if `sensitiveFields` is provided.

          sensitive_fields: Laravel-style dot-notated paths to fields to decrypt.

              - Same syntax and behavior as in EncryptRequest.
              - If omitted, all string values matching encryption prefix are attempted.

              Examples:

              - `user.ssn`
              - `employees.*.payroll.token`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            DecryptDecryptPayloadResponse,
            self._post(
                "/decrypt",
                body=maybe_transform(
                    {
                        "data": data,
                        "sensitive_fields": sensitive_fields,
                    },
                    decrypt_decrypt_payload_params.DecryptDecryptPayloadParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, DecryptDecryptPayloadResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncDecryptResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDecryptResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDecryptResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDecryptResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/qanapi/qanapi-sdk-python#with_streaming_response
        """
        return AsyncDecryptResourceWithStreamingResponse(self)

    async def decrypt_payload(
        self,
        *,
        data: Union[str, Dict[str, object], Iterable[object]],
        sensitive_fields: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DecryptDecryptPayloadResponse:
        """
        Decrypt encrypted payload

        Args:
          data: The encrypted payload to decrypt.

              - Can be a string or an object/array with encrypted fields.
              - Decryption is selective if `sensitiveFields` is provided.

          sensitive_fields: Laravel-style dot-notated paths to fields to decrypt.

              - Same syntax and behavior as in EncryptRequest.
              - If omitted, all string values matching encryption prefix are attempted.

              Examples:

              - `user.ssn`
              - `employees.*.payroll.token`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            DecryptDecryptPayloadResponse,
            await self._post(
                "/decrypt",
                body=await async_maybe_transform(
                    {
                        "data": data,
                        "sensitive_fields": sensitive_fields,
                    },
                    decrypt_decrypt_payload_params.DecryptDecryptPayloadParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, DecryptDecryptPayloadResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class DecryptResourceWithRawResponse:
    def __init__(self, decrypt: DecryptResource) -> None:
        self._decrypt = decrypt

        self.decrypt_payload = to_raw_response_wrapper(
            decrypt.decrypt_payload,
        )


class AsyncDecryptResourceWithRawResponse:
    def __init__(self, decrypt: AsyncDecryptResource) -> None:
        self._decrypt = decrypt

        self.decrypt_payload = async_to_raw_response_wrapper(
            decrypt.decrypt_payload,
        )


class DecryptResourceWithStreamingResponse:
    def __init__(self, decrypt: DecryptResource) -> None:
        self._decrypt = decrypt

        self.decrypt_payload = to_streamed_response_wrapper(
            decrypt.decrypt_payload,
        )


class AsyncDecryptResourceWithStreamingResponse:
    def __init__(self, decrypt: AsyncDecryptResource) -> None:
        self._decrypt = decrypt

        self.decrypt_payload = async_to_streamed_response_wrapper(
            decrypt.decrypt_payload,
        )
