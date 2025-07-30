# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from artemis import Artemis, AsyncArtemis
from tests.utils import assert_matches_type
from artemis.types import (
    AssetListAssetSymbolsResponse,
    AssetListSupportedMetricsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAsset:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_asset_symbols(self, client: Artemis) -> None:
        asset = client.asset.list_asset_symbols()
        assert_matches_type(AssetListAssetSymbolsResponse, asset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_asset_symbols(self, client: Artemis) -> None:
        response = client.asset.with_raw_response.list_asset_symbols()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        asset = response.parse()
        assert_matches_type(AssetListAssetSymbolsResponse, asset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_asset_symbols(self, client: Artemis) -> None:
        with client.asset.with_streaming_response.list_asset_symbols() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            asset = response.parse()
            assert_matches_type(AssetListAssetSymbolsResponse, asset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list_supported_metrics(self, client: Artemis) -> None:
        asset = client.asset.list_supported_metrics(
            symbol="symbol",
        )
        assert_matches_type(AssetListSupportedMetricsResponse, asset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_supported_metrics(self, client: Artemis) -> None:
        response = client.asset.with_raw_response.list_supported_metrics(
            symbol="symbol",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        asset = response.parse()
        assert_matches_type(AssetListSupportedMetricsResponse, asset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_supported_metrics(self, client: Artemis) -> None:
        with client.asset.with_streaming_response.list_supported_metrics(
            symbol="symbol",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            asset = response.parse()
            assert_matches_type(AssetListSupportedMetricsResponse, asset, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAsset:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_asset_symbols(self, async_client: AsyncArtemis) -> None:
        asset = await async_client.asset.list_asset_symbols()
        assert_matches_type(AssetListAssetSymbolsResponse, asset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_asset_symbols(self, async_client: AsyncArtemis) -> None:
        response = await async_client.asset.with_raw_response.list_asset_symbols()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        asset = await response.parse()
        assert_matches_type(AssetListAssetSymbolsResponse, asset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_asset_symbols(self, async_client: AsyncArtemis) -> None:
        async with async_client.asset.with_streaming_response.list_asset_symbols() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            asset = await response.parse()
            assert_matches_type(AssetListAssetSymbolsResponse, asset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_supported_metrics(self, async_client: AsyncArtemis) -> None:
        asset = await async_client.asset.list_supported_metrics(
            symbol="symbol",
        )
        assert_matches_type(AssetListSupportedMetricsResponse, asset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_supported_metrics(self, async_client: AsyncArtemis) -> None:
        response = await async_client.asset.with_raw_response.list_supported_metrics(
            symbol="symbol",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        asset = await response.parse()
        assert_matches_type(AssetListSupportedMetricsResponse, asset, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_supported_metrics(self, async_client: AsyncArtemis) -> None:
        async with async_client.asset.with_streaming_response.list_supported_metrics(
            symbol="symbol",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            asset = await response.parse()
            assert_matches_type(AssetListSupportedMetricsResponse, asset, path=["response"])

        assert cast(Any, response.is_closed) is True
