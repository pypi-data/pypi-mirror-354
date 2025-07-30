# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AssetListSupportedMetricsParams"]


class AssetListSupportedMetricsParams(TypedDict, total=False):
    symbol: Required[str]
    """Symbol"""
