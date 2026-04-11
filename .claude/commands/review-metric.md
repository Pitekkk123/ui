Review a specific metric from the macro snapshot system.

Given metric name "$ARGUMENTS":
1. Find the fetcher that produces this metric
2. Read the fetcher code and explain:
   - What data source it uses
   - What quality tier it is (A/B/C)
   - What methodology is applied
   - Whether the naming is honest (proxy vs official)
3. Check if there are any known issues or improvement opportunities
4. If the metric is a proxy, explain what the "real" version would be
