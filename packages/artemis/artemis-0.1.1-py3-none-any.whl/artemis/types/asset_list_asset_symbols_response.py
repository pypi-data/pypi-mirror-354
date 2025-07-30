# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["AssetListAssetSymbolsResponse", "AssetListAssetSymbolsResponseItem"]


class AssetListAssetSymbolsResponseItem(BaseModel):
    artemis_id: str

    coingecko_id: str

    color: str

    symbol: str

    title: str


AssetListAssetSymbolsResponse: TypeAlias = List[AssetListAssetSymbolsResponseItem]
