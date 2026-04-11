# Methodology — Macro Risk Overlay for Momentum Fund

## Purpose

This overlay provides a daily assessment of whether the macro environment
supports or threatens momentum strategies. It is NOT a directional trading
signal. It is a risk context layer that informs:

- Position sizing
- Breakout confidence
- Exposure management
- Regime classification

## Data Architecture

### Three-layer model

| Layer | Role | Example metrics |
|-------|------|-----------------|
| A. Short-term fuel | Is breadth supporting breakouts now? | McClellan Oscillator, TRIN, NH/NL |
| B. Medium-term regime | Is this still a healthy trend environment? | McClellan Summation, breadth deterioration |
| C. Systemic risk amplifier | Is the foundation unstable? | HY OAS, rate-vol proxy, VX curve, VVIX |

### Composite score

The environment score combines three sub-scores:

- **Credit (40%)**: HY OAS, IG OAS, NFCI
- **Rates (30%)**: 2s10s spread, 3m10y spread
- **Volatility (30%)**: VIX close, VVIX close

Only Tier A metrics with status "ok" contribute. If data is missing,
the score is based on fewer inputs (documented in the notes field).

Score range: -1.0 (maximum stress) to +1.0 (benign environment).

## Metric definitions

### FRED Series (Tier A)

| Metric | FRED ID | What it measures |
|--------|---------|------------------|
| hy_oas | BAMLH0A0HYM2 | High-yield corporate bond option-adjusted spread |
| ig_oas | BAMLC0A0CM | Investment-grade corporate bond OAS |
| nfci | NFCI | Chicago Fed National Financial Conditions Index |
| spread_2s10s | T10Y2Y | 10Y minus 2Y Treasury yield spread |
| spread_3m10y | T10Y3M | 10Y minus 3M Treasury yield spread |
| real_10y | DFII10 | 10Y TIPS yield (real rate) |
| breakeven_10y | T10YIE | 10Y breakeven inflation rate |
| vix_fred_close | VIXCLS | VIX close from FRED (cross-check) |
| dxy_broad | DTWEXBGS | Trade-weighted broad dollar index |

### Cboe Official (Tier A)

| Metric | Source | What it measures |
|--------|--------|------------------|
| vix_close | Cboe VIX History CSV | S&P 500 30-day implied volatility |
| vvix_close | Cboe VVIX History CSV | Volatility of VIX (vol-of-vol) |
| vx1_settlement | Cboe CFE (T+1) | Front-month VX futures settlement |
| vx2_settlement | Cboe CFE (T+1) | Second-month VX futures settlement |
| vx1_vx2_ratio | Derived | VX term structure shape indicator |

### Proxies (Tier B)

| Metric | Source | What it actually is | What it is NOT |
|--------|--------|---------------------|----------------|
| tlt_realized_vol_proxy | yfinance/TLT | 20d annualized realized vol of TLT ETF | ICE MOVE Index |
| spy_gamma_oi_proxy | Polygon/SPY | gamma * OI proxy from SPY option chain | Dealer gamma exposure / "GEX" |
| spx_gamma_oi_proxy | Polygon/I:SPX | gamma * OI proxy from SPX option chain | Full market maker net gamma |

### Breadth (Tier B, placeholder)

| Metric | Formula | Role |
|--------|---------|------|
| trin | (Adv/Dec) / (AdvVol/DecVol) | Intraday breadth pressure |
| mcclellan_oscillator | 19-EMA minus 39-EMA of net advances | Short-term breadth momentum |
| mcclellan_summation | Running cumulative total of Oscillator | Medium-term breadth regime |
| new_highs_minus_lows | NH - NL (52-week) | Leadership breadth |

### McClellan: critical distinctions

- **Oscillator** = 19-EMA(net_advances) - 39-EMA(net_advances)
  - Fast; measures breadth acceleration/deceleration
  - Good for: breakout confidence, thrust detection, exhaustion

- **Summation Index** = running cumulative total of Oscillator
  - Slow; measures accumulated breadth health
  - Good for: regime assessment, trend support, exposure decisions
  - Previous Summation + current Oscillator (NOT a rolling window sum)

- **Rolling sum** = sum of last N Oscillator values in a fixed window
  - Different indicator with different behavior
  - Must NEVER be labeled "McClellan Summation Index"

## Two-phase pipeline

### Phase 1: Preliminary snapshot (after US close)

Collects all available data. Some VX data may be preliminary.

### Phase 2: Official reconciliation (next business day ~10:00 CT)

Updates VX settlement curve with official Cboe futures stats.
Cboe CFE daily futures statistics are published approximately
10:00 a.m. CT the next business day.

## Naming policy

Every metric name must honestly reflect its data source and methodology:

- If it's a proxy, the name contains "proxy" (e.g., `tlt_realized_vol_proxy`)
- If it's derived, the methodology field says so
- If it's official, the source field points to the authoritative origin
- No metric may be named as if it represents something it doesn't
