#!/usr/bin/env python3
"""
Macro Indicators Snapshot — TickerLab Style

A comprehensive macro/sentiment data collector that fetches 19 indicator classes
from free sources (FRED, CBOE CDN, yfinance, Stooq) and produces a JSON snapshot
with signal analysis.

Usage:
    # Single run (default):
    python macro_snapshot.py

    # Run and schedule daily at 20:00 CET:
    python macro_snapshot.py --schedule

    # Run with custom output directory:
    MACRO_OUTPUT_DIR=/path/to/output python macro_snapshot.py

    # Skip slow fetchers (options chains):
    python macro_snapshot.py --fast

    # Pretty-print to console only:
    python macro_snapshot.py --print-only

Environment variables:
    FRED_API_KEY       — Your FRED API key (required for FRED data)
    MACRO_OUTPUT_DIR   — Directory for JSON output (default: script dir)
    MACRO_RUN_TIME     — Daily run time in HH:MM format (default: 20:00)
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Ensure the script directory is in the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import FRED_API_KEY, OUTPUT_DIR, SNAPSHOT_FILENAME, HISTORY_FILENAME, DAILY_RUN_TIME
from fetchers.fred import fetch_fred_snapshot
from fetchers.cboe import fetch_vix_vvix, fetch_vx_term_structure
from fetchers.yfinance_data import fetch_gex, fetch_options_flow, fetch_move_proxy
from fetchers.breadth import fetch_trin, fetch_hlli, fetch_mcclellan
from signals import (
    analyze_credit_stress,
    analyze_yield_curve,
    analyze_financial_conditions,
    analyze_dollar,
    generate_composite_signal,
)

logger = logging.getLogger("macro_snapshot")


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def collect_all_data(fast: bool = False) -> dict[str, Any]:
    """
    Collect data from all sources and run signal analysis.

    Args:
        fast: If True, skip slow operations (options chains for GEX/flow).
    """
    snapshot: dict[str, Any] = {
        "meta": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "sources": ["FRED", "CBOE CDN", "yfinance", "Stooq"],
        },
    }

    # ── 1. FRED (macro/credit/yields) ────────────────────────────────────
    if FRED_API_KEY and FRED_API_KEY != "YOUR_FRED_API_KEY_HERE":
        fred_data = fetch_fred_snapshot()
    else:
        logger.warning(
            "FRED_API_KEY not set — skipping FRED data. "
            "Register free at https://fred.stlouisfed.org/docs/api/api_key.html"
        )
        fred_data = {}
    snapshot["fred"] = fred_data

    # ── 2. CBOE (VIX, VVIX, VX term structure) ──────────────────────────
    cboe_data = fetch_vix_vvix()
    snapshot["cboe_vix_vvix"] = cboe_data

    vx_data = fetch_vx_term_structure()
    snapshot["cboe_vx_futures"] = vx_data

    # ── 3. yfinance-based indicators ─────────────────────────────────────
    if not fast:
        gex_data = fetch_gex()
        options_flow_data = fetch_options_flow()
    else:
        logger.info("Fast mode: skipping GEX and options flow (slow API calls)")
        gex_data = {"gex_total_billions": None, "gex_signal": "skipped (fast mode)"}
        options_flow_data = {}
    snapshot["gex"] = gex_data
    snapshot["options_flow"] = options_flow_data

    move_data = fetch_move_proxy()
    snapshot["move_proxy"] = move_data

    # ── 4. Breadth (TRIN, HLLI, McClellan) ───────────────────────────────
    trin_data = fetch_trin()
    snapshot["trin"] = trin_data

    hlli_data = fetch_hlli()
    snapshot["hlli"] = hlli_data

    mcclellan_data = fetch_mcclellan()
    snapshot["mcclellan"] = mcclellan_data

    # ── 5. Signal Analysis ───────────────────────────────────────────────
    analysis: dict[str, Any] = {}
    analysis["credit_stress"] = analyze_credit_stress(fred_data)
    analysis["yield_curve"] = analyze_yield_curve(fred_data)
    analysis["financial_conditions"] = analyze_financial_conditions(fred_data)
    analysis["dollar"] = analyze_dollar(fred_data)
    analysis["composite"] = generate_composite_signal(
        fred=fred_data,
        cboe=cboe_data,
        vx=vx_data,
        gex=gex_data,
        options_flow=options_flow_data,
        move=move_data,
        trin=trin_data,
        hlli=hlli_data,
        mcclellan=mcclellan_data,
    )
    snapshot["analysis"] = analysis

    return snapshot


def save_snapshot(snapshot: dict[str, Any], output_dir: str) -> str:
    """Save snapshot to JSON file. Returns the file path."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, SNAPSHOT_FILENAME)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, default=str, ensure_ascii=False)
    logger.info("Snapshot saved to %s", filepath)
    return filepath


def append_to_history(snapshot: dict[str, Any], output_dir: str) -> None:
    """Append snapshot to rolling history file (one entry per day)."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, HISTORY_FILENAME)

    history: list[dict[str, Any]] = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            logger.warning("Corrupted history file, starting fresh")
            history = []

    # Keep last 365 entries max
    history.append(snapshot)
    history = history[-365:]

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, default=str, ensure_ascii=False)
    logger.info("History updated (%d entries) at %s", len(history), filepath)


def print_summary(snapshot: dict[str, Any]) -> None:
    """Print a human-readable summary to console."""
    print("\n" + "=" * 70)
    print("  MACRO INDICATORS SNAPSHOT")
    print(f"  {snapshot['meta']['timestamp_utc']}")
    print("=" * 70)

    # FRED data
    fred = snapshot.get("fred", {})
    if fred:
        print("\n── FRED (Macro/Credit/Yields) ──────────────────────────────")
        for key, val in fred.items():
            if val is not None:
                print(f"  {key:20s}: {val}")
            else:
                print(f"  {key:20s}: N/A")

    # VIX/VVIX
    cboe = snapshot.get("cboe_vix_vvix", {})
    if cboe:
        print("\n── CBOE (VIX/VVIX) ────────────────────────────────────────")
        for key in ["vix", "vix_zone", "vvix", "vvix_zone", "vix_vvix_matrix"]:
            if key in cboe:
                print(f"  {key:20s}: {cboe[key]}")

    # VX term structure
    vx = snapshot.get("cboe_vx_futures", {})
    if vx:
        print("\n── VX Term Structure ──────────────────────────────────────")
        for key in ["vx1", "vx2", "vx_ratio", "term_structure"]:
            if key in vx:
                print(f"  {key:20s}: {vx[key]}")

    # GEX
    gex = snapshot.get("gex", {})
    if gex:
        print("\n── Gamma Exposure (GEX) ───────────────────────────────────")
        for key in ["gex_total_billions", "gex_signal", "spot_price"]:
            if key in gex:
                print(f"  {key:20s}: {gex[key]}")

    # Options flow
    flow = snapshot.get("options_flow", {})
    if flow:
        print("\n── Options Flow (P/C Ratios) ──────────────────────────────")
        for ticker, data in flow.items():
            if isinstance(data, dict):
                pc = data.get("pc_ratio", "N/A")
                sig = data.get("signal", "")
                print(f"  {ticker:6s}: P/C={pc}  {sig}")

    # MOVE proxy
    move = snapshot.get("move_proxy", {})
    if move:
        print("\n── MOVE Proxy (TLT Vol) ───────────────────────────────────")
        for key in ["tlt_realized_vol_20d", "move_proxy_signal"]:
            if key in move:
                print(f"  {key:20s}: {move[key]}")

    # Breadth
    for section, title in [
        ("trin", "TRIN (Arms Index)"),
        ("hlli", "HLLI (High-Low Leadership)"),
        ("mcclellan", "McClellan Oscillator"),
    ]:
        data = snapshot.get(section, {})
        if data:
            print(f"\n── {title} {'─' * (50 - len(title))}")
            for key, val in data.items():
                print(f"  {key:25s}: {val}")

    # Composite analysis
    analysis = snapshot.get("analysis", {})
    composite = analysis.get("composite", {})
    if composite:
        print("\n" + "=" * 70)
        print("  COMPOSITE SIGNAL")
        print("=" * 70)
        print(f"  Score:      {composite.get('composite_score', 'N/A')} / {composite.get('max_possible_score', 'N/A')}")
        print(f"  Normalized: {composite.get('normalized_score', 'N/A')}")
        print(f"  Regime:     {composite.get('regime', 'N/A')}")

        bullish = composite.get("bullish_factors", [])
        bearish = composite.get("bearish_factors", [])
        if bullish:
            print(f"  Bullish:    {', '.join(bullish)}")
        if bearish:
            print(f"  Bearish:    {', '.join(bearish)}")

    # Sub-analyses
    for key, title in [
        ("credit_stress", "Credit Stress"),
        ("yield_curve", "Yield Curve"),
        ("financial_conditions", "Financial Conditions"),
    ]:
        sub = analysis.get(key, {})
        if sub:
            print(f"\n── {title} {'─' * (50 - len(title))}")
            for k, v in sub.items():
                print(f"  {k:30s}: {v}")

    print("\n" + "=" * 70 + "\n")


def run_scheduled(fast: bool = False) -> None:
    """Run on a daily schedule using the `schedule` library."""
    try:
        import schedule
    except ImportError:
        logger.error("Install 'schedule' package: pip install schedule")
        sys.exit(1)

    def job():
        logger.info("Scheduled run starting...")
        snapshot = collect_all_data(fast=fast)
        save_snapshot(snapshot, OUTPUT_DIR)
        append_to_history(snapshot, OUTPUT_DIR)
        print_summary(snapshot)

    # Run immediately on start
    job()

    # Schedule daily
    schedule.every().day.at(DAILY_RUN_TIME).do(job)
    logger.info("Scheduled daily at %s. Press Ctrl+C to stop.", DAILY_RUN_TIME)

    while True:
        schedule.run_pending()
        time.sleep(60)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Macro Indicators Snapshot — collect & analyze market macro data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--schedule", action="store_true",
        help=f"Run daily at {DAILY_RUN_TIME} (configurable via MACRO_RUN_TIME env var)",
    )
    parser.add_argument(
        "--fast", action="store_true",
        help="Skip slow fetchers (GEX options chains, options flow)",
    )
    parser.add_argument(
        "--print-only", action="store_true",
        help="Print to console without saving JSON",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--output-dir", "-o", type=str, default=OUTPUT_DIR,
        help=f"Output directory for JSON files (default: {OUTPUT_DIR})",
    )
    args = parser.parse_args()

    setup_logging(args.verbose)

    if args.schedule:
        run_scheduled(fast=args.fast)
    else:
        snapshot = collect_all_data(fast=args.fast)

        if args.print_only:
            print_summary(snapshot)
        else:
            save_snapshot(snapshot, args.output_dir)
            append_to_history(snapshot, args.output_dir)
            print_summary(snapshot)


if __name__ == "__main__":
    main()
