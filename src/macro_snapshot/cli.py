"""CLI entry point for the macro risk overlay snapshot engine.

Usage:
    python -m macro_snapshot.cli                 # full prelim snapshot + save
    python -m macro_snapshot.cli --print-only    # print snapshot, don't save
    python -m macro_snapshot.cli --fast           # skip Polygon (FRED + Cboe only)
    python -m macro_snapshot.cli --reconcile-vx   # T+1 VX settlement reconcile
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys

from dotenv import load_dotenv

from macro_snapshot.pipeline import build_prelim_snapshot, build_reconciled_snapshot
from macro_snapshot.storage import append_to_history, save_snapshot_json

load_dotenv()


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Macro Risk Overlay Snapshot Engine for Momentum Fund",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print the snapshot to stdout without saving to disk.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Fast mode: skip Polygon gamma-OI proxy (FRED + Cboe only).",
    )
    parser.add_argument(
        "--reconcile-vx",
        action="store_true",
        help="Run T+1 VX settlement reconciliation instead of prelim snapshot.",
    )
    parser.add_argument(
        "--data-dir",
        default=os.environ.get("DATA_DIR", "./data"),
        help="Directory for snapshot output files (default: ./data).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )

    args = parser.parse_args()
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger("macro_snapshot.cli")

    if args.reconcile_vx:
        logger.info("Running T+1 VX settlement reconciliation...")
        snap = build_reconciled_snapshot()
    else:
        polygon_key = None if args.fast else os.environ.get("POLYGON_API_KEY")
        logger.info(
            "Building prelim snapshot (fast=%s, polygon=%s)...",
            args.fast,
            "configured" if polygon_key else "not configured",
        )
        snap = build_prelim_snapshot(polygon_api_key=polygon_key)

    if args.print_only:
        print(json.dumps(snap.to_dict(), indent=2, default=str))
        return

    json_path = save_snapshot_json(snap, data_dir=args.data_dir)
    parquet_path = append_to_history(snap, data_dir=args.data_dir)

    # Summary
    total = len(snap.metrics)
    ok_count = sum(1 for m in snap.metrics.values() if m.get("status") == "ok")
    stale_count = sum(1 for m in snap.metrics.values() if m.get("is_stale"))
    proxy_count = sum(1 for m in snap.metrics.values() if m.get("status") == "proxy")

    env_score = snap.metrics.get("environment_score", {}).get("value")

    logger.info("=" * 60)
    logger.info("Snapshot complete: %s", snap.phase)
    logger.info("  Total metrics: %d", total)
    logger.info("  OK: %d | Stale: %d | Proxy: %d", ok_count, stale_count, proxy_count)
    if env_score is not None:
        logger.info("  Environment score: %.3f", env_score)
    logger.info("  JSON: %s", json_path)
    logger.info("  Parquet: %s", parquet_path)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
