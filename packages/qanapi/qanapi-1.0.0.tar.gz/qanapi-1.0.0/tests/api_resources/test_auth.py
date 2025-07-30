# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from qanapi import Qanapi, AsyncQanapi
from tests.utils import assert_matches_type
from qanapi.types import (
    AuthLoginResponse,
    AuthLogoutResponse,
    AuthRevokeTokenResponse,
    AuthRefreshTokenResponse,
    AuthRetrieveUserDetailsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAuth:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_login(self, client: Qanapi) -> None:
        auth = client.auth.login(
            email="valid@email.com",
            password="secret123",
        )
        assert_matches_type(AuthLoginResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_login(self, client: Qanapi) -> None:
        response = client.auth.with_raw_response.login(
            email="valid@email.com",
            password="secret123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(AuthLoginResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_login(self, client: Qanapi) -> None:
        with client.auth.with_streaming_response.login(
            email="valid@email.com",
            password="secret123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(AuthLoginResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_logout(self, client: Qanapi) -> None:
        auth = client.auth.logout()
        assert_matches_type(AuthLogoutResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_logout(self, client: Qanapi) -> None:
        response = client.auth.with_raw_response.logout()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(AuthLogoutResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_logout(self, client: Qanapi) -> None:
        with client.auth.with_streaming_response.logout() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(AuthLogoutResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_refresh_token(self, client: Qanapi) -> None:
        auth = client.auth.refresh_token()
        assert_matches_type(AuthRefreshTokenResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_refresh_token(self, client: Qanapi) -> None:
        response = client.auth.with_raw_response.refresh_token()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(AuthRefreshTokenResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_refresh_token(self, client: Qanapi) -> None:
        with client.auth.with_streaming_response.refresh_token() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(AuthRefreshTokenResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_user_details(self, client: Qanapi) -> None:
        auth = client.auth.retrieve_user_details()
        assert_matches_type(AuthRetrieveUserDetailsResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_user_details(self, client: Qanapi) -> None:
        response = client.auth.with_raw_response.retrieve_user_details()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(AuthRetrieveUserDetailsResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_user_details(self, client: Qanapi) -> None:
        with client.auth.with_streaming_response.retrieve_user_details() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(AuthRetrieveUserDetailsResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_revoke_token(self, client: Qanapi) -> None:
        auth = client.auth.revoke_token()
        assert_matches_type(AuthRevokeTokenResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_revoke_token(self, client: Qanapi) -> None:
        response = client.auth.with_raw_response.revoke_token()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = response.parse()
        assert_matches_type(AuthRevokeTokenResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_revoke_token(self, client: Qanapi) -> None:
        with client.auth.with_streaming_response.revoke_token() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = response.parse()
            assert_matches_type(AuthRevokeTokenResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAuth:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_login(self, async_client: AsyncQanapi) -> None:
        auth = await async_client.auth.login(
            email="valid@email.com",
            password="secret123",
        )
        assert_matches_type(AuthLoginResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_login(self, async_client: AsyncQanapi) -> None:
        response = await async_client.auth.with_raw_response.login(
            email="valid@email.com",
            password="secret123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(AuthLoginResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_login(self, async_client: AsyncQanapi) -> None:
        async with async_client.auth.with_streaming_response.login(
            email="valid@email.com",
            password="secret123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(AuthLoginResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_logout(self, async_client: AsyncQanapi) -> None:
        auth = await async_client.auth.logout()
        assert_matches_type(AuthLogoutResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_logout(self, async_client: AsyncQanapi) -> None:
        response = await async_client.auth.with_raw_response.logout()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(AuthLogoutResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_logout(self, async_client: AsyncQanapi) -> None:
        async with async_client.auth.with_streaming_response.logout() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(AuthLogoutResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_refresh_token(self, async_client: AsyncQanapi) -> None:
        auth = await async_client.auth.refresh_token()
        assert_matches_type(AuthRefreshTokenResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_refresh_token(self, async_client: AsyncQanapi) -> None:
        response = await async_client.auth.with_raw_response.refresh_token()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(AuthRefreshTokenResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_refresh_token(self, async_client: AsyncQanapi) -> None:
        async with async_client.auth.with_streaming_response.refresh_token() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(AuthRefreshTokenResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_user_details(self, async_client: AsyncQanapi) -> None:
        auth = await async_client.auth.retrieve_user_details()
        assert_matches_type(AuthRetrieveUserDetailsResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_user_details(self, async_client: AsyncQanapi) -> None:
        response = await async_client.auth.with_raw_response.retrieve_user_details()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(AuthRetrieveUserDetailsResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_user_details(self, async_client: AsyncQanapi) -> None:
        async with async_client.auth.with_streaming_response.retrieve_user_details() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(AuthRetrieveUserDetailsResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_revoke_token(self, async_client: AsyncQanapi) -> None:
        auth = await async_client.auth.revoke_token()
        assert_matches_type(AuthRevokeTokenResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_revoke_token(self, async_client: AsyncQanapi) -> None:
        response = await async_client.auth.with_raw_response.revoke_token()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auth = await response.parse()
        assert_matches_type(AuthRevokeTokenResponse, auth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_revoke_token(self, async_client: AsyncQanapi) -> None:
        async with async_client.auth.with_streaming_response.revoke_token() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auth = await response.parse()
            assert_matches_type(AuthRevokeTokenResponse, auth, path=["response"])

        assert cast(Any, response.is_closed) is True
