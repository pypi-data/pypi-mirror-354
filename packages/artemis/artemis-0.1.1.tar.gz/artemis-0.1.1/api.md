# Artemis

Types:

```python
from artemis.types import (
    FetchMetricsResponse,
    FetchWeeklyActiveDevsResponse,
    FetchWeeklyCommitsResponse,
    ListEcosystemsResponse,
)
```

Methods:

- <code title="get /data/{metricNames}">client.<a href="./src/artemis/_client.py">fetch_metrics</a>(metric_names, \*\*<a href="src/artemis/types/client_fetch_metrics_params.py">params</a>) -> <a href="./src/artemis/types/fetch_metrics_response.py">FetchMetricsResponse</a></code>
- <code title="get /weekly-active-devs">client.<a href="./src/artemis/_client.py">fetch_weekly_active_devs</a>(\*\*<a href="src/artemis/types/client_fetch_weekly_active_devs_params.py">params</a>) -> <a href="./src/artemis/types/fetch_weekly_active_devs_response.py">FetchWeeklyActiveDevsResponse</a></code>
- <code title="get /weekly-commits">client.<a href="./src/artemis/_client.py">fetch_weekly_commits</a>(\*\*<a href="src/artemis/types/client_fetch_weekly_commits_params.py">params</a>) -> <a href="./src/artemis/types/fetch_weekly_commits_response.py">FetchWeeklyCommitsResponse</a></code>
- <code title="get /dev-ecosystems">client.<a href="./src/artemis/_client.py">list_ecosystems</a>() -> <a href="./src/artemis/types/list_ecosystems_response.py">ListEcosystemsResponse</a></code>

# Asset

Types:

```python
from artemis.types import AssetListAssetSymbolsResponse, AssetListSupportedMetricsResponse
```

Methods:

- <code title="get /asset-symbols">client.asset.<a href="./src/artemis/resources/asset.py">list_asset_symbols</a>() -> <a href="./src/artemis/types/asset_list_asset_symbols_response.py">AssetListAssetSymbolsResponse</a></code>
- <code title="get /supported-metrics/">client.asset.<a href="./src/artemis/resources/asset.py">list_supported_metrics</a>(\*\*<a href="src/artemis/types/asset_list_supported_metrics_params.py">params</a>) -> <a href="./src/artemis/types/asset_list_supported_metrics_response.py">AssetListSupportedMetricsResponse</a></code>
