# Macro Risk Overlay — Project Memory

## What this project is

A daily macro risk overlay engine for a momentum fund. It builds an auditable
snapshot of credit, rates, volatility, and breadth conditions, with explicit
data quality tiers and honest proxy labeling.

## Architecture

```
fetchers/  -->  pipeline.py  -->  signals.py  -->  storage.py
  fred.py          |                  |              |
  cboe.py      Snapshot          composite       JSON + parquet
  polygon_options.py            environment
  proxies.py                    score + flags
  breadth.py
```

### Two-phase pipeline

1. **prelim_snapshot** — run after US market close. Collects FRED, Cboe VIX/VVIX,
   TLT proxy, Polygon gamma-OI proxy, breadth placeholders.
2. **official_reconcile** — run next business day ~10:00 CT. Updates VX settlement
   curve with official Cboe futures data (published with T+1 delay).

### Data quality tiers

- **Tier A**: Official, auditable sources (FRED series, Cboe official CSVs)
- **Tier B**: Useful proxies or delayed public data (TLT realized vol, gamma-OI proxy)
- **Tier C**: Exploratory / unverified

### Critical naming conventions

- `spy_gamma_oi_proxy` — NOT "GEX". It's gamma*OI from ETF chain, not dealer book.
- `tlt_realized_vol_proxy` — NOT "MOVE". It's realized vol of TLT, not ICE implied rate vol.
- `mcclellan_summation` — ONLY for running cumulative total of Oscillator, never rolling sum.

## Key files

| File | Purpose |
|------|---------|
| `src/macro_snapshot/schemas.py` | MetricPoint dataclass with full provenance |
| `src/macro_snapshot/fetchers/fred.py` | FRED series (HY OAS, IG OAS, NFCI, curves, DXY) |
| `src/macro_snapshot/fetchers/cboe.py` | Official Cboe VIX/VVIX CSVs + VX settlement |
| `src/macro_snapshot/fetchers/polygon_options.py` | Gamma-OI proxy from Polygon/Massive |
| `src/macro_snapshot/fetchers/proxies.py` | TLT realized vol proxy |
| `src/macro_snapshot/fetchers/breadth.py` | Breadth indicators (placeholder until verified feed) |
| `src/macro_snapshot/pipeline.py` | Orchestrator: prelim + reconcile phases |
| `src/macro_snapshot/signals.py` | Composite environment score + flag lists |
| `src/macro_snapshot/storage.py` | JSON + parquet persistence |
| `src/macro_snapshot/cli.py` | CLI entry point |

## Commands

```bash
python -m macro_snapshot.cli                  # full prelim snapshot + save
python -m macro_snapshot.cli --print-only     # print without saving
python -m macro_snapshot.cli --fast           # skip Polygon (FRED + Cboe only)
python -m macro_snapshot.cli --reconcile-vx   # T+1 VX settlement reconcile
```

## Rules for modifications

1. Every metric MUST return a MetricPoint with full metadata (value, asof, source, status, quality_tier, methodology).
2. Never label a proxy as an official metric. Names must reflect the actual data source.
3. Breadth is excluded from hard composite score until a verified A/D + NH/NL feed is connected.
4. McClellan Summation = cumulative total of Oscillator. Rolling sum is a DIFFERENT indicator.
5. Composite score uses ONLY Tier A metrics with status=ok.
6. Tests must use mocks — no real network requests in unit tests.
