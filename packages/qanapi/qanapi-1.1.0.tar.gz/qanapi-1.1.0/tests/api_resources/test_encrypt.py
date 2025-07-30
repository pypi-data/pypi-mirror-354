# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from qanapi import Qanapi, AsyncQanapi
from tests.utils import assert_matches_type
from qanapi.types import EncryptEncryptDataResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEncrypt:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_encrypt_data(self, client: Qanapi) -> None:
        encrypt = client.encrypt.encrypt_data(
            data={"password": "bar"},
        )
        assert_matches_type(EncryptEncryptDataResponse, encrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_encrypt_data_with_all_params(self, client: Qanapi) -> None:
        encrypt = client.encrypt.encrypt_data(
            data={"password": "bar"},
            access={"acl": ["admin"]},
            attributes={
                "classification": "confidential",
                "owner": "alice@example.com",
                "tags": ["legal"],
            },
            sensitive_fields=["password"],
        )
        assert_matches_type(EncryptEncryptDataResponse, encrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_encrypt_data(self, client: Qanapi) -> None:
        response = client.encrypt.with_raw_response.encrypt_data(
            data={"password": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        encrypt = response.parse()
        assert_matches_type(EncryptEncryptDataResponse, encrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_encrypt_data(self, client: Qanapi) -> None:
        with client.encrypt.with_streaming_response.encrypt_data(
            data={"password": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            encrypt = response.parse()
            assert_matches_type(EncryptEncryptDataResponse, encrypt, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEncrypt:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_encrypt_data(self, async_client: AsyncQanapi) -> None:
        encrypt = await async_client.encrypt.encrypt_data(
            data={"password": "bar"},
        )
        assert_matches_type(EncryptEncryptDataResponse, encrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_encrypt_data_with_all_params(self, async_client: AsyncQanapi) -> None:
        encrypt = await async_client.encrypt.encrypt_data(
            data={"password": "bar"},
            access={"acl": ["admin"]},
            attributes={
                "classification": "confidential",
                "owner": "alice@example.com",
                "tags": ["legal"],
            },
            sensitive_fields=["password"],
        )
        assert_matches_type(EncryptEncryptDataResponse, encrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_encrypt_data(self, async_client: AsyncQanapi) -> None:
        response = await async_client.encrypt.with_raw_response.encrypt_data(
            data={"password": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        encrypt = await response.parse()
        assert_matches_type(EncryptEncryptDataResponse, encrypt, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_encrypt_data(self, async_client: AsyncQanapi) -> None:
        async with async_client.encrypt.with_streaming_response.encrypt_data(
            data={"password": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            encrypt = await response.parse()
            assert_matches_type(EncryptEncryptDataResponse, encrypt, path=["response"])

        assert cast(Any, response.is_closed) is True
