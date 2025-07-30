# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from qanapi import Qanapi, AsyncQanapi
from tests.utils import assert_matches_type
from qanapi.types import (
    ScopeListResponse,
    ScopeCreateResponse,
    ScopeDeleteResponse,
    ScopeUpdateResponse,
    ScopeRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestScopes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Qanapi) -> None:
        scope = client.scopes.create(
            name="read:secrets",
            route="decrypt",
        )
        assert_matches_type(ScopeCreateResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Qanapi) -> None:
        response = client.scopes.with_raw_response.create(
            name="read:secrets",
            route="decrypt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = response.parse()
        assert_matches_type(ScopeCreateResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Qanapi) -> None:
        with client.scopes.with_streaming_response.create(
            name="read:secrets",
            route="decrypt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = response.parse()
            assert_matches_type(ScopeCreateResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Qanapi) -> None:
        scope = client.scopes.retrieve(
            0,
        )
        assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Qanapi) -> None:
        response = client.scopes.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = response.parse()
        assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Qanapi) -> None:
        with client.scopes.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = response.parse()
            assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Qanapi) -> None:
        scope = client.scopes.update(
            id=0,
        )
        assert_matches_type(ScopeUpdateResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: Qanapi) -> None:
        scope = client.scopes.update(
            id=0,
            name="read:secrets",
            route="decrypt",
        )
        assert_matches_type(ScopeUpdateResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Qanapi) -> None:
        response = client.scopes.with_raw_response.update(
            id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = response.parse()
        assert_matches_type(ScopeUpdateResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Qanapi) -> None:
        with client.scopes.with_streaming_response.update(
            id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = response.parse()
            assert_matches_type(ScopeUpdateResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Qanapi) -> None:
        scope = client.scopes.list()
        assert_matches_type(ScopeListResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Qanapi) -> None:
        response = client.scopes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = response.parse()
        assert_matches_type(ScopeListResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Qanapi) -> None:
        with client.scopes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = response.parse()
            assert_matches_type(ScopeListResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Qanapi) -> None:
        scope = client.scopes.delete(
            0,
        )
        assert_matches_type(ScopeDeleteResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Qanapi) -> None:
        response = client.scopes.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = response.parse()
        assert_matches_type(ScopeDeleteResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Qanapi) -> None:
        with client.scopes.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = response.parse()
            assert_matches_type(ScopeDeleteResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncScopes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncQanapi) -> None:
        scope = await async_client.scopes.create(
            name="read:secrets",
            route="decrypt",
        )
        assert_matches_type(ScopeCreateResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncQanapi) -> None:
        response = await async_client.scopes.with_raw_response.create(
            name="read:secrets",
            route="decrypt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = await response.parse()
        assert_matches_type(ScopeCreateResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncQanapi) -> None:
        async with async_client.scopes.with_streaming_response.create(
            name="read:secrets",
            route="decrypt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = await response.parse()
            assert_matches_type(ScopeCreateResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncQanapi) -> None:
        scope = await async_client.scopes.retrieve(
            0,
        )
        assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncQanapi) -> None:
        response = await async_client.scopes.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = await response.parse()
        assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncQanapi) -> None:
        async with async_client.scopes.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = await response.parse()
            assert_matches_type(ScopeRetrieveResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncQanapi) -> None:
        scope = await async_client.scopes.update(
            id=0,
        )
        assert_matches_type(ScopeUpdateResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncQanapi) -> None:
        scope = await async_client.scopes.update(
            id=0,
            name="read:secrets",
            route="decrypt",
        )
        assert_matches_type(ScopeUpdateResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncQanapi) -> None:
        response = await async_client.scopes.with_raw_response.update(
            id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = await response.parse()
        assert_matches_type(ScopeUpdateResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncQanapi) -> None:
        async with async_client.scopes.with_streaming_response.update(
            id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = await response.parse()
            assert_matches_type(ScopeUpdateResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncQanapi) -> None:
        scope = await async_client.scopes.list()
        assert_matches_type(ScopeListResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncQanapi) -> None:
        response = await async_client.scopes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = await response.parse()
        assert_matches_type(ScopeListResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncQanapi) -> None:
        async with async_client.scopes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = await response.parse()
            assert_matches_type(ScopeListResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncQanapi) -> None:
        scope = await async_client.scopes.delete(
            0,
        )
        assert_matches_type(ScopeDeleteResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncQanapi) -> None:
        response = await async_client.scopes.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scope = await response.parse()
        assert_matches_type(ScopeDeleteResponse, scope, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncQanapi) -> None:
        async with async_client.scopes.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scope = await response.parse()
            assert_matches_type(ScopeDeleteResponse, scope, path=["response"])

        assert cast(Any, response.is_closed) is True
