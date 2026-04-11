"""Persistence layer — JSON snapshots and parquet history.

Writes:
  - data/latest_snapshot.json  (most recent full snapshot)
  - data/history.parquet       (append-only time series of all snapshots)

The JSON file is designed to be human-readable and directly consumable
by Claude for risk interpretation. The parquet file is for backtesting
and percentile analysis.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

import pandas as pd

from macro_snapshot.schemas import Snapshot

logger = logging.getLogger(__name__)

DEFAULT_DATA_DIR = os.environ.get("DATA_DIR", "./data")


def save_snapshot_json(
    snap: Snapshot,
    data_dir: str = DEFAULT_DATA_DIR,
) -> Path:
    """Write the latest snapshot as pretty-printed JSON."""
    path = Path(data_dir)
    path.mkdir(parents=True, exist_ok=True)

    out_file = path / "latest_snapshot.json"
    with open(out_file, "w") as f:
        json.dump(snap.to_dict(), f, indent=2, default=str)

    logger.info("Saved snapshot to %s", out_file)
    return out_file


def append_to_history(
    snap: Snapshot,
    data_dir: str = DEFAULT_DATA_DIR,
) -> Path:
    """Append snapshot metrics to the parquet history file.

    Each row is one metric from one snapshot, keyed by
    (timestamp, metric_name).
    """
    path = Path(data_dir)
    path.mkdir(parents=True, exist_ok=True)

    parquet_file = path / "history.parquet"

    rows: list[dict[str, Any]] = []
    for name, m in snap.metrics.items():
        rows.append(
            {
                "timestamp": snap.timestamp,
                "phase": snap.phase,
                "metric_name": name,
                "value": m.get("value"),
                "asof": m.get("asof"),
                "source": m.get("source"),
                "status": m.get("status"),
                "is_stale": m.get("is_stale"),
                "quality_tier": m.get("quality_tier"),
                "methodology": m.get("methodology"),
                "notes": m.get("notes"),
            }
        )

    new_df = pd.DataFrame(rows)

    if parquet_file.exists():
        try:
            existing = pd.read_parquet(parquet_file)
            combined = pd.concat([existing, new_df], ignore_index=True)
        except Exception:
            logger.warning("Could not read existing parquet; overwriting.")
            combined = new_df
    else:
        combined = new_df

    combined.to_parquet(parquet_file, index=False)
    logger.info("Appended %d rows to %s", len(rows), parquet_file)
    return parquet_file
