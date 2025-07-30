# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from artemis import Artemis, AsyncArtemis
from tests.utils import assert_matches_type
from artemis.types import (
    FetchMetricsResponse,
    ListEcosystemsResponse,
    FetchWeeklyCommitsResponse,
    FetchWeeklyActiveDevsResponse,
)
from artemis._utils import parse_date

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClient:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_fetch_metrics(self, client: Artemis) -> None:
        client_ = client.fetch_metrics(
            metric_names="price,mc",
            symbols="symbols",
        )
        assert_matches_type(FetchMetricsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_fetch_metrics_with_all_params(self, client: Artemis) -> None:
        client_ = client.fetch_metrics(
            metric_names="price,mc",
            symbols="symbols",
            end_date=parse_date("2019-12-27"),
            start_date=parse_date("2019-12-27"),
            summarize=True,
        )
        assert_matches_type(FetchMetricsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_fetch_metrics(self, client: Artemis) -> None:
        response = client.with_raw_response.fetch_metrics(
            metric_names="price,mc",
            symbols="symbols",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(FetchMetricsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_fetch_metrics(self, client: Artemis) -> None:
        with client.with_streaming_response.fetch_metrics(
            metric_names="price,mc",
            symbols="symbols",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(FetchMetricsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_fetch_metrics(self, client: Artemis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_names` but received ''"):
            client.with_raw_response.fetch_metrics(
                metric_names="",
                symbols="symbols",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_fetch_weekly_active_devs(self, client: Artemis) -> None:
        client_ = client.fetch_weekly_active_devs()
        assert_matches_type(FetchWeeklyActiveDevsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_fetch_weekly_active_devs_with_all_params(self, client: Artemis) -> None:
        client_ = client.fetch_weekly_active_devs(
            days_back=0,
            ecosystem="ecosystem",
            include_forks=True,
        )
        assert_matches_type(FetchWeeklyActiveDevsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_fetch_weekly_active_devs(self, client: Artemis) -> None:
        response = client.with_raw_response.fetch_weekly_active_devs()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(FetchWeeklyActiveDevsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_fetch_weekly_active_devs(self, client: Artemis) -> None:
        with client.with_streaming_response.fetch_weekly_active_devs() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(FetchWeeklyActiveDevsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_fetch_weekly_commits(self, client: Artemis) -> None:
        client_ = client.fetch_weekly_commits()
        assert_matches_type(FetchWeeklyCommitsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_fetch_weekly_commits_with_all_params(self, client: Artemis) -> None:
        client_ = client.fetch_weekly_commits(
            days_back=0,
            ecosystem="ecosystem",
            include_forks=True,
        )
        assert_matches_type(FetchWeeklyCommitsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_fetch_weekly_commits(self, client: Artemis) -> None:
        response = client.with_raw_response.fetch_weekly_commits()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(FetchWeeklyCommitsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_fetch_weekly_commits(self, client: Artemis) -> None:
        with client.with_streaming_response.fetch_weekly_commits() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(FetchWeeklyCommitsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list_ecosystems(self, client: Artemis) -> None:
        client_ = client.list_ecosystems()
        assert_matches_type(ListEcosystemsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_ecosystems(self, client: Artemis) -> None:
        response = client.with_raw_response.list_ecosystems()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(ListEcosystemsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_ecosystems(self, client: Artemis) -> None:
        with client.with_streaming_response.list_ecosystems() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(ListEcosystemsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncClient:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_fetch_metrics(self, async_client: AsyncArtemis) -> None:
        client = await async_client.fetch_metrics(
            metric_names="price,mc",
            symbols="symbols",
        )
        assert_matches_type(FetchMetricsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_fetch_metrics_with_all_params(self, async_client: AsyncArtemis) -> None:
        client = await async_client.fetch_metrics(
            metric_names="price,mc",
            symbols="symbols",
            end_date=parse_date("2019-12-27"),
            start_date=parse_date("2019-12-27"),
            summarize=True,
        )
        assert_matches_type(FetchMetricsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_fetch_metrics(self, async_client: AsyncArtemis) -> None:
        response = await async_client.with_raw_response.fetch_metrics(
            metric_names="price,mc",
            symbols="symbols",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(FetchMetricsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_fetch_metrics(self, async_client: AsyncArtemis) -> None:
        async with async_client.with_streaming_response.fetch_metrics(
            metric_names="price,mc",
            symbols="symbols",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(FetchMetricsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_fetch_metrics(self, async_client: AsyncArtemis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_names` but received ''"):
            await async_client.with_raw_response.fetch_metrics(
                metric_names="",
                symbols="symbols",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_fetch_weekly_active_devs(self, async_client: AsyncArtemis) -> None:
        client = await async_client.fetch_weekly_active_devs()
        assert_matches_type(FetchWeeklyActiveDevsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_fetch_weekly_active_devs_with_all_params(self, async_client: AsyncArtemis) -> None:
        client = await async_client.fetch_weekly_active_devs(
            days_back=0,
            ecosystem="ecosystem",
            include_forks=True,
        )
        assert_matches_type(FetchWeeklyActiveDevsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_fetch_weekly_active_devs(self, async_client: AsyncArtemis) -> None:
        response = await async_client.with_raw_response.fetch_weekly_active_devs()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(FetchWeeklyActiveDevsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_fetch_weekly_active_devs(self, async_client: AsyncArtemis) -> None:
        async with async_client.with_streaming_response.fetch_weekly_active_devs() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(FetchWeeklyActiveDevsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_fetch_weekly_commits(self, async_client: AsyncArtemis) -> None:
        client = await async_client.fetch_weekly_commits()
        assert_matches_type(FetchWeeklyCommitsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_fetch_weekly_commits_with_all_params(self, async_client: AsyncArtemis) -> None:
        client = await async_client.fetch_weekly_commits(
            days_back=0,
            ecosystem="ecosystem",
            include_forks=True,
        )
        assert_matches_type(FetchWeeklyCommitsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_fetch_weekly_commits(self, async_client: AsyncArtemis) -> None:
        response = await async_client.with_raw_response.fetch_weekly_commits()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(FetchWeeklyCommitsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_fetch_weekly_commits(self, async_client: AsyncArtemis) -> None:
        async with async_client.with_streaming_response.fetch_weekly_commits() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(FetchWeeklyCommitsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_ecosystems(self, async_client: AsyncArtemis) -> None:
        client = await async_client.list_ecosystems()
        assert_matches_type(ListEcosystemsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_ecosystems(self, async_client: AsyncArtemis) -> None:
        response = await async_client.with_raw_response.list_ecosystems()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(ListEcosystemsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_ecosystems(self, async_client: AsyncArtemis) -> None:
        async with async_client.with_streaming_response.list_ecosystems() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(ListEcosystemsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True
