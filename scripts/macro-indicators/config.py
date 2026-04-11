"""
Configuration for Macro Indicators Script.
Set your API keys and preferences here.
"""

import os
from datetime import date

# ── FRED API ──────────────────────────────────────────────────────────────────
# Register for free at: https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY = os.environ.get("FRED_API_KEY", "YOUR_FRED_API_KEY_HERE")

# ── Date range ────────────────────────────────────────────────────────────────
DATA_START_DATE = date(2020, 1, 1)

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_DIR = os.environ.get("MACRO_OUTPUT_DIR", os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_FILENAME = "macro_snapshot.json"
HISTORY_FILENAME = "macro_history.json"

# ── Schedule (24h format, CET) ────────────────────────────────────────────────
DAILY_RUN_TIME = os.environ.get("MACRO_RUN_TIME", "20:00")

# ── FRED Series IDs ───────────────────────────────────────────────────────────
FRED_SERIES = {
    "hy_oas":           "BAMLH0A0HYM2",   # ICE BofA US High Yield OAS
    "ig_oas":           "BAMLC0A0CM",      # ICE BofA US IG Corporate OAS
    "nfci":             "NFCI",            # Chicago Fed National Financial Conditions
    "anfci":            "ANFCI",           # Adjusted NFCI
    "treasury_3m":      "DTB3",            # 3-Month T-Bill
    "treasury_2y":      "DGS2",            # 2-Year Treasury yield
    "treasury_10y":     "DGS10",           # 10-Year Treasury yield
    "treasury_30y":     "DGS30",           # 30-Year Treasury yield
    "spread_3m10y":     "T10Y3M",          # 10Y minus 3M spread
    "spread_2s10s":     "T10Y2Y",          # 10Y minus 2Y spread
    "tips_10y_real":    "DFII10",          # 10-Year TIPS real yield
    "breakeven_10y":    "T10YIE",          # 10-Year Breakeven inflation
    "breakeven_5y":     "T5YIE",           # 5-Year Breakeven
    "cp_tbill_spread":  "CPFF",            # Commercial Paper Funding Facility proxy
    "dxy_broad":        "DTWEXBGS",        # Broad Trade-Weighted Dollar Index
    "vix_fred":         "VIXCLS",          # CBOE VIX closing (T+1 lag)
}

# ── CBOE direct CSV URLs ─────────────────────────────────────────────────────
CBOE_VIX_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"
CBOE_VVIX_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VVIX_History.csv"
CBOE_VX_FUTURES_URL = "https://cdn.cboe.com/api/global/futures_and_options/daily_market_data/VX_{ym}.csv"

# ── Options flow tickers ──────────────────────────────────────────────────────
OPTIONS_FLOW_TICKERS = ["TLT", "SQQQ", "UVXY", "VXX", "SDS"]

# ── GEX calculation ──────────────────────────────────────────────────────────
GEX_TICKER = "SPY"
GEX_NUM_EXPIRIES = 3

# ── MOVE proxy ────────────────────────────────────────────────────────────────
MOVE_PROXY_TICKER = "TLT"
MOVE_PROXY_WINDOW = 20  # days for realized vol

# ── Breadth data (Stooq) ─────────────────────────────────────────────────────
STOOQ_TRIN_URL = "https://stooq.com/q/d/l/?s=$trin&d1={start}&d2={end}&i=d"
STOOQ_NYHL_URL = "https://stooq.com/q/d/l/?s=$nyhl&d1={start}&d2={end}&i=d"  # NYSE new highs
STOOQ_NYLO_URL = "https://stooq.com/q/d/l/?s=$nylo&d1={start}&d2={end}&i=d"  # NYSE new lows

# ── Signal thresholds ────────────────────────────────────────────────────────
THRESHOLDS = {
    "vix": {"low": 15, "mid": 22, "high": 30},
    "vvix": {"low": 90, "mid": 110, "high": 120},
    "hy_oas": {"low": 300, "mid": 450, "high": 600},
    "ig_oas": {"low": 80, "mid": 130, "high": 200},
    "nfci": {"tight": -0.5, "neutral": 0, "loose": 0.5},
    "trin": {"extreme_bull": 0.5, "neutral_low": 0.8, "neutral_high": 1.2, "extreme_bear": 2.0},
    "gex_billions": {"negative": 0, "low": 2, "high": 5},
    "spread_2s10s": {"inverted": 0, "flat": 0.25, "steep": 1.0},
    "breakeven_10y": {"deflation_risk": 1.5, "anchored_low": 2.0, "anchored_high": 2.5, "overheating": 3.0},
    "move_proxy": {"calm": 10, "elevated": 15, "stress": 20},
}
