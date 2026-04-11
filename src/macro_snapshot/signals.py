"""Signal computation — composite environment score and flag lists.

The composite score is intentionally simple at this stage.
It uses ONLY Tier A metrics with status "ok" to avoid inflating
confidence with proxy or stale data.

Output:
  - environment_score: -1.0 (maximum stress) to +1.0 (benign)
  - bullish_flags: list of supportive conditions
  - bearish_flags: list of warning conditions
  - proxy_flags: list of metrics that are proxy/derived
  - stale_flags: list of metrics that are stale or missing
"""

from __future__ import annotations

import json
from typing import Any

from macro_snapshot.schemas import (
    STATUS_OK,
    STATUS_PROXY,
    STATUS_STALE,
    TIER_A,
    MetricPoint,
    Snapshot,
)


# ── Threshold definitions ──────────────────────────────────────────
# These are deliberately conservative starting points. Adjust based on
# historical percentile analysis of your own data.

THRESHOLDS = {
    "hy_oas": {"stress": 5.0, "elevated": 4.0, "benign": 3.5},
    "ig_oas": {"stress": 1.8, "elevated": 1.3, "benign": 1.0},
    "nfci": {"stress": 0.5, "elevated": 0.0, "benign": -0.5},
    "spread_2s10s": {"inversion": 0.0},
    "spread_3m10y": {"inversion": 0.0},
    "vix_close": {"stress": 30, "elevated": 20, "benign": 15},
    "vvix_close": {"stress": 120, "elevated": 100, "benign": 90},
}


def _get_value(snap: Snapshot, name: str) -> float | None:
    """Extract a metric value from the snapshot if it's ok and Tier A."""
    m = snap.metrics.get(name)
    if m is None:
        return None
    if m.get("status") not in (STATUS_OK,):
        return None
    return m.get("value")


def _score_credit(snap: Snapshot) -> tuple[float, list[str], list[str]]:
    """Score credit conditions: HY OAS + IG OAS + NFCI."""
    score = 0.0
    bullish: list[str] = []
    bearish: list[str] = []
    count = 0

    hy = _get_value(snap, "hy_oas")
    if hy is not None:
        count += 1
        t = THRESHOLDS["hy_oas"]
        if hy >= t["stress"]:
            score -= 1.0
            bearish.append(f"HY OAS stress ({hy:.2f} >= {t['stress']})")
        elif hy >= t["elevated"]:
            score -= 0.5
            bearish.append(f"HY OAS elevated ({hy:.2f})")
        elif hy <= t["benign"]:
            score += 0.5
            bullish.append(f"HY OAS benign ({hy:.2f})")

    ig = _get_value(snap, "ig_oas")
    if ig is not None:
        count += 1
        t = THRESHOLDS["ig_oas"]
        if ig >= t["stress"]:
            score -= 1.0
            bearish.append(f"IG OAS stress ({ig:.2f} >= {t['stress']})")
        elif ig >= t["elevated"]:
            score -= 0.5
            bearish.append(f"IG OAS elevated ({ig:.2f})")
        elif ig <= t["benign"]:
            score += 0.5
            bullish.append(f"IG OAS benign ({ig:.2f})")

    nfci = _get_value(snap, "nfci")
    if nfci is not None:
        count += 1
        t = THRESHOLDS["nfci"]
        if nfci >= t["stress"]:
            score -= 1.0
            bearish.append(f"NFCI tightening ({nfci:.3f} >= {t['stress']})")
        elif nfci >= t["elevated"]:
            score -= 0.3
            bearish.append(f"NFCI neutral-tight ({nfci:.3f})")
        elif nfci <= t["benign"]:
            score += 0.5
            bullish.append(f"NFCI loose ({nfci:.3f})")

    if count > 0:
        score /= count
    return score, bullish, bearish


def _score_rates(snap: Snapshot) -> tuple[float, list[str], list[str]]:
    """Score rates/curve conditions: 2s10s, 3m10y, real10Y, breakeven."""
    score = 0.0
    bullish: list[str] = []
    bearish: list[str] = []
    count = 0

    for spread_name in ("spread_2s10s", "spread_3m10y"):
        val = _get_value(snap, spread_name)
        if val is not None:
            count += 1
            if val < THRESHOLDS[spread_name]["inversion"]:
                score -= 1.0
                bearish.append(f"{spread_name} inverted ({val:.2f})")
            else:
                score += 0.3
                bullish.append(f"{spread_name} positive ({val:.2f})")

    if count > 0:
        score /= count
    return score, bullish, bearish


def _score_vol(snap: Snapshot) -> tuple[float, list[str], list[str]]:
    """Score volatility conditions: VIX + VVIX."""
    score = 0.0
    bullish: list[str] = []
    bearish: list[str] = []
    count = 0

    vix = _get_value(snap, "vix_close")
    if vix is not None:
        count += 1
        t = THRESHOLDS["vix_close"]
        if vix >= t["stress"]:
            score -= 1.0
            bearish.append(f"VIX stress ({vix:.1f} >= {t['stress']})")
        elif vix >= t["elevated"]:
            score -= 0.5
            bearish.append(f"VIX elevated ({vix:.1f})")
        elif vix <= t["benign"]:
            score += 0.5
            bullish.append(f"VIX benign ({vix:.1f})")

    vvix = _get_value(snap, "vvix_close")
    if vvix is not None:
        count += 1
        t = THRESHOLDS["vvix_close"]
        if vvix >= t["stress"]:
            score -= 1.0
            bearish.append(f"VVIX stress ({vvix:.1f} >= {t['stress']})")
        elif vvix >= t["elevated"]:
            score -= 0.3
            bearish.append(f"VVIX elevated ({vvix:.1f})")
        elif vvix <= t["benign"]:
            score += 0.3
            bullish.append(f"VVIX benign ({vvix:.1f})")

    if count > 0:
        score /= count
    return score, bullish, bearish


def _collect_flags(snap: Snapshot) -> tuple[list[str], list[str]]:
    """Collect proxy and stale flags across all metrics."""
    proxy_flags: list[str] = []
    stale_flags: list[str] = []

    for name, m in snap.metrics.items():
        status = m.get("status", "")
        if status == STATUS_PROXY:
            proxy_flags.append(f"{name}: {m.get('methodology', 'proxy')}")
        if status in (STATUS_STALE, "no_data", "error"):
            stale_flags.append(f"{name}: {status}")

    return proxy_flags, stale_flags


def compute_signals(snap: Snapshot) -> list[MetricPoint]:
    """Compute composite environment score and flag lists.

    Only Tier A metrics with status=ok are used in the composite.
    Proxy and breadth metrics are flagged but not scored.
    """
    credit_score, credit_bull, credit_bear = _score_credit(snap)
    rates_score, rates_bull, rates_bear = _score_rates(snap)
    vol_score, vol_bull, vol_bear = _score_vol(snap)

    # Weighted composite: credit 40%, rates 30%, vol 30%
    composite = credit_score * 0.4 + rates_score * 0.3 + vol_score * 0.3
    composite = max(-1.0, min(1.0, composite))

    all_bullish = credit_bull + rates_bull + vol_bull
    all_bearish = credit_bear + rates_bear + vol_bear
    proxy_flags, stale_flags = _collect_flags(snap)

    # Count how many Tier A metrics contributed
    tier_a_ok = sum(
        1
        for m in snap.metrics.values()
        if m.get("quality_tier") == TIER_A and m.get("status") == STATUS_OK
    )

    return [
        MetricPoint(
            name="environment_score",
            value=round(composite, 3),
            asof=None,
            source="signals:composite",
            status="ok",
            is_stale=False,
            notes=(
                f"Composite: credit={credit_score:.2f}*0.4 + "
                f"rates={rates_score:.2f}*0.3 + vol={vol_score:.2f}*0.3. "
                f"Based on {tier_a_ok} Tier-A ok metrics."
            ),
            quality_tier=TIER_A,
            methodology="weighted_composite",
        ),
        MetricPoint(
            name="bullish_flags",
            value=float(len(all_bullish)),
            asof=None,
            source="signals:flags",
            status="ok",
            is_stale=False,
            notes=json.dumps(all_bullish),
            quality_tier=TIER_A,
            methodology="flag_list",
        ),
        MetricPoint(
            name="bearish_flags",
            value=float(len(all_bearish)),
            asof=None,
            source="signals:flags",
            status="ok",
            is_stale=False,
            notes=json.dumps(all_bearish),
            quality_tier=TIER_A,
            methodology="flag_list",
        ),
        MetricPoint(
            name="proxy_flags",
            value=float(len(proxy_flags)),
            asof=None,
            source="signals:flags",
            status="ok",
            is_stale=False,
            notes=json.dumps(proxy_flags),
            quality_tier=TIER_A,
            methodology="flag_list",
        ),
        MetricPoint(
            name="stale_flags",
            value=float(len(stale_flags)),
            asof=None,
            source="signals:flags",
            status="ok",
            is_stale=False,
            notes=json.dumps(stale_flags),
            quality_tier=TIER_A,
            methodology="flag_list",
        ),
    ]
