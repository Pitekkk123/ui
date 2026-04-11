# Data Quality Policy

## Core principle

The system must never silently hide data quality issues. Every metric
carries its own provenance metadata. The composite score explicitly
counts how many Tier A metrics contributed, so users know what the
score is based on.

## Quality tiers

### Tier A — Official, auditable

Sources where the data provenance is clear and the feed is stable:

- FRED series via pandas-datareader
- Cboe official CSV files (VIX/VVIX history)
- Cboe CFE official settlement data

**Rule**: Tier A data goes directly into the composite score.

### Tier B — Useful proxy or delayed

Sources that are directionally useful but have known limitations:

- TLT realized vol (proxy for rate-vol, not MOVE)
- Gamma * OI proxy from Polygon (proxy for dealer gamma, not "GEX")
- Breadth indicators from non-verified feeds
- MOVE from public delayed pages (monitoring only)

**Rule**: Tier B data is displayed in the snapshot with clear proxy
labeling. It is NOT included in the hard composite score. It may
contribute to flag lists (proxy_flags).

### Tier C — Exploratory

Sources that haven't been validated for production use:

- Any new provider before verification
- Community APIs without documented SLAs

**Rule**: Tier C data must not appear in production snapshots.

## Status codes

| Status | Meaning | Composite inclusion |
|--------|---------|---------------------|
| ok | Fresh, valid data | Yes (if Tier A) |
| stale | Data older than threshold | No |
| no_data | Empty or missing | No |
| error | Fetch/parse failure | No |
| proxy | Derived/approximate | No (flagged only) |

## Staleness rules

- FRED series: stale if latest observation is > 5 calendar days old
- Cboe VIX/VVIX: stale if latest close is > 5 calendar days old
- Proxies: staleness follows their underlying data source
- Breadth: not evaluated until verified feed is connected

## MetricPoint contract

Every fetcher must return MetricPoints with ALL fields populated:

```python
MetricPoint(
    name="metric_name",          # honest, descriptive name
    value=42.0,                  # float or None
    asof="2026-04-10",           # ISO date of the observation
    source="FRED:SYMBOL",        # authoritative source identifier
    status="ok",                 # ok | stale | no_data | error | proxy
    is_stale=False,              # boolean convenience flag
    notes="...",                  # human-readable context
    quality_tier="A",            # A | B | C
    methodology="official_series", # how the value was obtained
)
```

## What NOT to do

1. **Never label a proxy as official.** If it's gamma*OI from an ETF chain,
   it's `spy_gamma_oi_proxy`, not `gex`.

2. **Never label TLT vol as MOVE.** MOVE is implied vol on rates/swaptions.
   TLT realized vol is a different measurement of a related concept.

3. **Never use rolling sum as McClellan Summation.** The classic Summation
   Index is a running cumulative total. A rolling window sum is a different
   indicator with different behavior.

4. **Never include stale/proxy data in the composite score** without
   explicitly documenting the degradation.

5. **Never skip the status field.** A metric without status metadata
   is worse than no metric at all.
