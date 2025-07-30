# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from qanapi import Qanapi, AsyncQanapi
from tests.utils import assert_matches_type
from qanapi.types import APIKeyRevokeResponse, APIKeyRotateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAPIKeys:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_revoke(self, client: Qanapi) -> None:
        api_key = client.api_keys.revoke(
            "apiKey",
        )
        assert_matches_type(APIKeyRevokeResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_revoke(self, client: Qanapi) -> None:
        response = client.api_keys.with_raw_response.revoke(
            "apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(APIKeyRevokeResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_revoke(self, client: Qanapi) -> None:
        with client.api_keys.with_streaming_response.revoke(
            "apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(APIKeyRevokeResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_revoke(self, client: Qanapi) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_key` but received ''"):
            client.api_keys.with_raw_response.revoke(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_rotate(self, client: Qanapi) -> None:
        api_key = client.api_keys.rotate(
            "apiKey",
        )
        assert_matches_type(APIKeyRotateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_rotate(self, client: Qanapi) -> None:
        response = client.api_keys.with_raw_response.rotate(
            "apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = response.parse()
        assert_matches_type(APIKeyRotateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_rotate(self, client: Qanapi) -> None:
        with client.api_keys.with_streaming_response.rotate(
            "apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = response.parse()
            assert_matches_type(APIKeyRotateResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_rotate(self, client: Qanapi) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_key` but received ''"):
            client.api_keys.with_raw_response.rotate(
                "",
            )


class TestAsyncAPIKeys:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_revoke(self, async_client: AsyncQanapi) -> None:
        api_key = await async_client.api_keys.revoke(
            "apiKey",
        )
        assert_matches_type(APIKeyRevokeResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_revoke(self, async_client: AsyncQanapi) -> None:
        response = await async_client.api_keys.with_raw_response.revoke(
            "apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(APIKeyRevokeResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_revoke(self, async_client: AsyncQanapi) -> None:
        async with async_client.api_keys.with_streaming_response.revoke(
            "apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(APIKeyRevokeResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_revoke(self, async_client: AsyncQanapi) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_key` but received ''"):
            await async_client.api_keys.with_raw_response.revoke(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_rotate(self, async_client: AsyncQanapi) -> None:
        api_key = await async_client.api_keys.rotate(
            "apiKey",
        )
        assert_matches_type(APIKeyRotateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_rotate(self, async_client: AsyncQanapi) -> None:
        response = await async_client.api_keys.with_raw_response.rotate(
            "apiKey",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        api_key = await response.parse()
        assert_matches_type(APIKeyRotateResponse, api_key, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_rotate(self, async_client: AsyncQanapi) -> None:
        async with async_client.api_keys.with_streaming_response.rotate(
            "apiKey",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            api_key = await response.parse()
            assert_matches_type(APIKeyRotateResponse, api_key, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_rotate(self, async_client: AsyncQanapi) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `api_key` but received ''"):
            await async_client.api_keys.with_raw_response.rotate(
                "",
            )
