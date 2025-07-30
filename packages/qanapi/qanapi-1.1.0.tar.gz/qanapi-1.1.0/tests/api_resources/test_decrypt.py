# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from qanapi import Qanapi, AsyncQanapi
from tests.utils import assert_matches_type
from qanapi.types import DecryptDecryptPayloadResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDecrypt:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_decrypt_payload(self, client: Qanapi) -> None:
        decrypt = client.decrypt.decrypt_payload(
            data={"password": "bar"},
        )
        assert_matches_type(DecryptDecryptPayloadResponse, decrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_decrypt_payload_with_all_params(self, client: Qanapi) -> None:
        decrypt = client.decrypt.decrypt_payload(
            data={"password": "bar"},
            sensitive_fields=["password"],
        )
        assert_matches_type(DecryptDecryptPayloadResponse, decrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_decrypt_payload(self, client: Qanapi) -> None:
        response = client.decrypt.with_raw_response.decrypt_payload(
            data={"password": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        decrypt = response.parse()
        assert_matches_type(DecryptDecryptPayloadResponse, decrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_decrypt_payload(self, client: Qanapi) -> None:
        with client.decrypt.with_streaming_response.decrypt_payload(
            data={"password": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            decrypt = response.parse()
            assert_matches_type(DecryptDecryptPayloadResponse, decrypt, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDecrypt:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_decrypt_payload(self, async_client: AsyncQanapi) -> None:
        decrypt = await async_client.decrypt.decrypt_payload(
            data={"password": "bar"},
        )
        assert_matches_type(DecryptDecryptPayloadResponse, decrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_decrypt_payload_with_all_params(self, async_client: AsyncQanapi) -> None:
        decrypt = await async_client.decrypt.decrypt_payload(
            data={"password": "bar"},
            sensitive_fields=["password"],
        )
        assert_matches_type(DecryptDecryptPayloadResponse, decrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_decrypt_payload(self, async_client: AsyncQanapi) -> None:
        response = await async_client.decrypt.with_raw_response.decrypt_payload(
            data={"password": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        decrypt = await response.parse()
        assert_matches_type(DecryptDecryptPayloadResponse, decrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_decrypt_payload(self, async_client: AsyncQanapi) -> None:
        async with async_client.decrypt.with_streaming_response.decrypt_payload(
            data={"password": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            decrypt = await response.parse()
            assert_matches_type(DecryptDecryptPayloadResponse, decrypt, path=["response"])

        assert cast(Any, response.is_closed) is True
