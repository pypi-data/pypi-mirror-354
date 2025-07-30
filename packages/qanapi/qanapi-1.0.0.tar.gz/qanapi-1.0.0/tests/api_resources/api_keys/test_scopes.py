# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from qanapi import Qanapi, AsyncQanapi
from tests.utils import assert_matches_type
from qanapi.types.api_keys import (
    ScopeSyncResponse,
    ScopeAttachResponse,
    ScopeDetachResponse,
    ScopeRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestScopes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Qanapi) -> None:
        scope = client.api_keys.scopes.retrieve(
            0,
        )
        assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Qanapi) -> None:
        response = client.api_keys.scopes.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = response.parse()
        assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Qanapi) -> None:
        with client.api_keys.scopes.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = response.parse()
            assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_attach(self, client: Qanapi) -> None:
        scope = client.api_keys.scopes.attach(
            api_key=0,
            scope_ids=[25],
        )
        assert_matches_type(ScopeAttachResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_attach(self, client: Qanapi) -> None:
        response = client.api_keys.scopes.with_raw_response.attach(
            api_key=0,
            scope_ids=[25],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = response.parse()
        assert_matches_type(ScopeAttachResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_attach(self, client: Qanapi) -> None:
        with client.api_keys.scopes.with_streaming_response.attach(
            api_key=0,
            scope_ids=[25],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = response.parse()
            assert_matches_type(ScopeAttachResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_detach(self, client: Qanapi) -> None:
        scope = client.api_keys.scopes.detach(
            api_key=0,
            scope_ids=[1],
        )
        assert_matches_type(ScopeDetachResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_detach(self, client: Qanapi) -> None:
        response = client.api_keys.scopes.with_raw_response.detach(
            api_key=0,
            scope_ids=[1],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = response.parse()
        assert_matches_type(ScopeDetachResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_detach(self, client: Qanapi) -> None:
        with client.api_keys.scopes.with_streaming_response.detach(
            api_key=0,
            scope_ids=[1],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = response.parse()
            assert_matches_type(ScopeDetachResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_sync(self, client: Qanapi) -> None:
        scope = client.api_keys.scopes.sync(
            api_key=0,
            scope_ids=[25],
        )
        assert_matches_type(ScopeSyncResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_sync(self, client: Qanapi) -> None:
        response = client.api_keys.scopes.with_raw_response.sync(
            api_key=0,
            scope_ids=[25],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = response.parse()
        assert_matches_type(ScopeSyncResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_sync(self, client: Qanapi) -> None:
        with client.api_keys.scopes.with_streaming_response.sync(
            api_key=0,
            scope_ids=[25],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = response.parse()
            assert_matches_type(ScopeSyncResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncScopes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncQanapi) -> None:
        scope = await async_client.api_keys.scopes.retrieve(
            0,
        )
        assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncQanapi) -> None:
        response = await async_client.api_keys.scopes.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = await response.parse()
        assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncQanapi) -> None:
        async with async_client.api_keys.scopes.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = await response.parse()
            assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_attach(self, async_client: AsyncQanapi) -> None:
        scope = await async_client.api_keys.scopes.attach(
            api_key=0,
            scope_ids=[25],
        )
        assert_matches_type(ScopeAttachResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_attach(self, async_client: AsyncQanapi) -> None:
        response = await async_client.api_keys.scopes.with_raw_response.attach(
            api_key=0,
            scope_ids=[25],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = await response.parse()
        assert_matches_type(ScopeAttachResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_attach(self, async_client: AsyncQanapi) -> None:
        async with async_client.api_keys.scopes.with_streaming_response.attach(
            api_key=0,
            scope_ids=[25],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = await response.parse()
            assert_matches_type(ScopeAttachResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_detach(self, async_client: AsyncQanapi) -> None:
        scope = await async_client.api_keys.scopes.detach(
            api_key=0,
            scope_ids=[1],
        )
        assert_matches_type(ScopeDetachResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_detach(self, async_client: AsyncQanapi) -> None:
        response = await async_client.api_keys.scopes.with_raw_response.detach(
            api_key=0,
            scope_ids=[1],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = await response.parse()
        assert_matches_type(ScopeDetachResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_detach(self, async_client: AsyncQanapi) -> None:
        async with async_client.api_keys.scopes.with_streaming_response.detach(
            api_key=0,
            scope_ids=[1],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = await response.parse()
            assert_matches_type(ScopeDetachResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_sync(self, async_client: AsyncQanapi) -> None:
        scope = await async_client.api_keys.scopes.sync(
            api_key=0,
            scope_ids=[25],
        )
        assert_matches_type(ScopeSyncResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_sync(self, async_client: AsyncQanapi) -> None:
        response = await async_client.api_keys.scopes.with_raw_response.sync(
            api_key=0,
            scope_ids=[25],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = await response.parse()
        assert_matches_type(ScopeSyncResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_sync(self, async_client: AsyncQanapi) -> None:
        async with async_client.api_keys.scopes.with_streaming_response.sync(
            api_key=0,
            scope_ids=[25],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = await response.parse()
            assert_matches_type(ScopeSyncResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True
