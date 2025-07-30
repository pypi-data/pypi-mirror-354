# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import asset_list_supported_metrics_params
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
from ..types.asset_list_asset_symbols_response import AssetListAssetSymbolsResponse
from ..types.asset_list_supported_metrics_response import AssetListSupportedMetricsResponse

__all__ = ["AssetResource", "AsyncAssetResource"]


class AssetResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AssetResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Artemis-xyz/artemis#accessing-raw-response-data-eg-headers
        """
        return AssetResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AssetResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Artemis-xyz/artemis#with_streaming_response
        """
        return AssetResourceWithStreamingResponse(self)

    def list_asset_symbols(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AssetListAssetSymbolsResponse:
        """List Supported Assets"""
        return self._get(
            "/asset-symbols",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AssetListAssetSymbolsResponse,
        )

    def list_supported_metrics(
        self,
        *,
        symbol: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AssetListSupportedMetricsResponse:
        """
        List available metrics for asset using symbol.

        Args:
          symbol: Symbol

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/supported-metrics/",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"symbol": symbol}, asset_list_supported_metrics_params.AssetListSupportedMetricsParams
                ),
            ),
            cast_to=AssetListSupportedMetricsResponse,
        )


class AsyncAssetResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAssetResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Artemis-xyz/artemis#accessing-raw-response-data-eg-headers
        """
        return AsyncAssetResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAssetResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Artemis-xyz/artemis#with_streaming_response
        """
        return AsyncAssetResourceWithStreamingResponse(self)

    async def list_asset_symbols(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AssetListAssetSymbolsResponse:
        """List Supported Assets"""
        return await self._get(
            "/asset-symbols",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AssetListAssetSymbolsResponse,
        )

    async def list_supported_metrics(
        self,
        *,
        symbol: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AssetListSupportedMetricsResponse:
        """
        List available metrics for asset using symbol.

        Args:
          symbol: Symbol

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/supported-metrics/",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"symbol": symbol}, asset_list_supported_metrics_params.AssetListSupportedMetricsParams
                ),
            ),
            cast_to=AssetListSupportedMetricsResponse,
        )


class AssetResourceWithRawResponse:
    def __init__(self, asset: AssetResource) -> None:
        self._asset = asset

        self.list_asset_symbols = to_raw_response_wrapper(
            asset.list_asset_symbols,
        )
        self.list_supported_metrics = to_raw_response_wrapper(
            asset.list_supported_metrics,
        )


class AsyncAssetResourceWithRawResponse:
    def __init__(self, asset: AsyncAssetResource) -> None:
        self._asset = asset

        self.list_asset_symbols = async_to_raw_response_wrapper(
            asset.list_asset_symbols,
        )
        self.list_supported_metrics = async_to_raw_response_wrapper(
            asset.list_supported_metrics,
        )


class AssetResourceWithStreamingResponse:
    def __init__(self, asset: AssetResource) -> None:
        self._asset = asset

        self.list_asset_symbols = to_streamed_response_wrapper(
            asset.list_asset_symbols,
        )
        self.list_supported_metrics = to_streamed_response_wrapper(
            asset.list_supported_metrics,
        )


class AsyncAssetResourceWithStreamingResponse:
    def __init__(self, asset: AsyncAssetResource) -> None:
        self._asset = asset

        self.list_asset_symbols = async_to_streamed_response_wrapper(
            asset.list_asset_symbols,
        )
        self.list_supported_metrics = async_to_streamed_response_wrapper(
            asset.list_supported_metrics,
        )
