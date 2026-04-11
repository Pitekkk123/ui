"""
Signal analysis and interpretation engine.

Takes raw indicator data from all fetchers and produces a unified
risk/sentiment assessment with actionable signals.
"""

import logging
from typing import Any

from config import THRESHOLDS

logger = logging.getLogger(__name__)


def _classify(value: float | None, thresholds: dict, labels: list[str]) -> str:
    """Classify a value against ordered thresholds."""
    if value is None:
        return "no_data"
    sorted_keys = sorted(thresholds.keys(), key=lambda k: thresholds[k])
    for i, key in enumerate(sorted_keys):
        if value < thresholds[key]:
            return labels[i] if i < len(labels) else labels[-1]
    return labels[-1] if labels else "unknown"


def analyze_credit_stress(fred: dict[str, Any]) -> dict[str, Any]:
    """Analyze credit spreads for stress signals."""
    result: dict[str, Any] = {}

    hy = fred.get("hy_oas")
    ig = fred.get("ig_oas")

    if hy is not None:
        if hy < 300:
            result["hy_oas_signal"] = "tight (risk-on, complacent)"
        elif hy < 450:
            result["hy_oas_signal"] = "normal"
        elif hy < 600:
            result["hy_oas_signal"] = "widening (stress building)"
        else:
            result["hy_oas_signal"] = "blown out (credit crisis territory)"

    if ig is not None:
        if ig < 80:
            result["ig_oas_signal"] = "tight (risk-on)"
        elif ig < 130:
            result["ig_oas_signal"] = "normal"
        elif ig < 200:
            result["ig_oas_signal"] = "widening"
        else:
            result["ig_oas_signal"] = "stress (flight to quality)"

    # HY-IG spread differential
    if hy is not None and ig is not None:
        diff = hy - ig
        result["hy_ig_differential"] = round(diff, 1)
        if diff > 400:
            result["credit_quality_signal"] = "high dispersion (risk aversion in junk)"
        elif diff > 250:
            result["credit_quality_signal"] = "normal differentiation"
        else:
            result["credit_quality_signal"] = "compressed (everyone reaching for yield)"

    return result


def analyze_yield_curve(fred: dict[str, Any]) -> dict[str, Any]:
    """Analyze yield curve shape and implications."""
    result: dict[str, Any] = {}

    s2s10 = fred.get("spread_2s10s")
    s3m10 = fred.get("spread_3m10y")

    if s2s10 is not None:
        if s2s10 < -0.5:
            result["curve_2s10s_signal"] = "deeply inverted (recession warning)"
        elif s2s10 < 0:
            result["curve_2s10s_signal"] = "inverted (slowdown expected)"
        elif s2s10 < 0.25:
            result["curve_2s10s_signal"] = "flat (late cycle)"
        elif s2s10 < 1.0:
            result["curve_2s10s_signal"] = "normal steepness"
        else:
            result["curve_2s10s_signal"] = "steep (early recovery or easing)"

    if s3m10 is not None:
        if s3m10 < -0.5:
            result["curve_3m10y_signal"] = "deeply inverted (strongest recession predictor)"
        elif s3m10 < 0:
            result["curve_3m10y_signal"] = "inverted"
        else:
            result["curve_3m10y_signal"] = "normal"

    # Real yield analysis
    real_10y = fred.get("tips_10y_real")
    if real_10y is not None:
        if real_10y < 0:
            result["real_yield_signal"] = "negative (financial repression, bullish risk assets)"
        elif real_10y < 1.0:
            result["real_yield_signal"] = "low positive (accommodative)"
        elif real_10y < 2.0:
            result["real_yield_signal"] = "moderate (tightening)"
        else:
            result["real_yield_signal"] = "restrictive (headwind for equities)"

    # Inflation expectations
    be10 = fred.get("breakeven_10y")
    be5 = fred.get("breakeven_5y")
    if be10 is not None:
        if be10 < 1.5:
            result["inflation_expectations"] = "deflation risk"
        elif be10 < 2.0:
            result["inflation_expectations"] = "below target (dovish Fed)"
        elif be10 < 2.5:
            result["inflation_expectations"] = "anchored (healthy)"
        elif be10 < 3.0:
            result["inflation_expectations"] = "above target (hawkish Fed)"
        else:
            result["inflation_expectations"] = "unanchored (stagflation risk)"

    if be10 is not None and be5 is not None:
        result["5y_10y_breakeven_diff"] = round(be10 - be5, 3)

    return result


def analyze_financial_conditions(fred: dict[str, Any]) -> dict[str, Any]:
    """Analyze NFCI / ANFCI signals."""
    result: dict[str, Any] = {}

    nfci = fred.get("nfci")
    anfci = fred.get("anfci")

    if nfci is not None:
        if nfci < -0.5:
            result["nfci_signal"] = "very loose (risk-on, leveraging)"
        elif nfci < 0:
            result["nfci_signal"] = "loose (accommodative)"
        elif nfci < 0.5:
            result["nfci_signal"] = "tightening"
        else:
            result["nfci_signal"] = "tight (stress, deleveraging)"

    if anfci is not None:
        result["anfci_signal"] = (
            "above avg tightening" if anfci > 0 else "below avg (loose)"
        )

    return result


def analyze_dollar(fred: dict[str, Any]) -> dict[str, Any]:
    """Analyze dollar strength implications."""
    result: dict[str, Any] = {}
    dxy = fred.get("dxy_broad")
    if dxy is not None:
        result["dxy_broad_value"] = round(dxy, 2)
        # DXY broad index is indexed, typical range 110-130
        result["dollar_note"] = (
            "Strong dollar = headwind for EM, commodities, multinationals. "
            "Weak dollar = tailwind for risk assets."
        )
    return result


def generate_composite_signal(
    fred: dict[str, Any],
    cboe: dict[str, Any],
    vx: dict[str, Any],
    gex: dict[str, Any],
    options_flow: dict[str, Any],
    move: dict[str, Any],
    trin: dict[str, Any],
    hlli: dict[str, Any],
    mcclellan: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate a composite risk/sentiment score from all indicators.

    Scoring: each indicator contributes -2 to +2.
    Negative = risk-off / bearish. Positive = risk-on / bullish.
    """
    scores: list[tuple[str, int]] = []

    # VIX
    vix = cboe.get("vix")
    if vix is not None:
        if vix < 15:
            scores.append(("VIX", 2))
        elif vix < 22:
            scores.append(("VIX", 1))
        elif vix < 30:
            scores.append(("VIX", -1))
        else:
            scores.append(("VIX", -2))

    # VVIX
    vvix = cboe.get("vvix")
    if vvix is not None:
        if vvix < 90:
            scores.append(("VVIX", 1))
        elif vvix < 110:
            scores.append(("VVIX", 0))
        else:
            scores.append(("VVIX", -1))

    # VX term structure
    vx_ratio = vx.get("vx_ratio")
    if vx_ratio is not None:
        if vx_ratio < 0.95:
            scores.append(("VX_term", 1))   # contango = normal
        elif vx_ratio > 1.05:
            scores.append(("VX_term", -2))   # backwardation = fear
        else:
            scores.append(("VX_term", 0))

    # Credit spreads
    hy = fred.get("hy_oas")
    if hy is not None:
        if hy < 300:
            scores.append(("HY_OAS", 2))
        elif hy < 450:
            scores.append(("HY_OAS", 1))
        elif hy < 600:
            scores.append(("HY_OAS", -1))
        else:
            scores.append(("HY_OAS", -2))

    # Yield curve 2s10s
    s2s10 = fred.get("spread_2s10s")
    if s2s10 is not None:
        if s2s10 < -0.5:
            scores.append(("Curve_2s10s", -2))
        elif s2s10 < 0:
            scores.append(("Curve_2s10s", -1))
        elif s2s10 < 1.0:
            scores.append(("Curve_2s10s", 1))
        else:
            scores.append(("Curve_2s10s", 2))

    # NFCI
    nfci = fred.get("nfci")
    if nfci is not None:
        if nfci < -0.5:
            scores.append(("NFCI", 2))
        elif nfci < 0:
            scores.append(("NFCI", 1))
        elif nfci < 0.5:
            scores.append(("NFCI", -1))
        else:
            scores.append(("NFCI", -2))

    # GEX
    gex_val = gex.get("gex_total_billions")
    if gex_val is not None:
        if gex_val > 2:
            scores.append(("GEX", 1))
        elif gex_val < 0:
            scores.append(("GEX", -1))
        else:
            scores.append(("GEX", 0))

    # MOVE proxy
    move_vol = move.get("tlt_realized_vol_20d")
    if move_vol is not None:
        if move_vol < 10:
            scores.append(("MOVE_proxy", 1))
        elif move_vol < 15:
            scores.append(("MOVE_proxy", 0))
        elif move_vol < 20:
            scores.append(("MOVE_proxy", -1))
        else:
            scores.append(("MOVE_proxy", -2))

    # TRIN
    trin_val = trin.get("trin")
    if trin_val is not None:
        if trin_val < 0.8:
            scores.append(("TRIN", 1))
        elif trin_val <= 1.2:
            scores.append(("TRIN", 0))
        elif trin_val <= 2.0:
            scores.append(("TRIN", -1))
        else:
            scores.append(("TRIN", -2))

    # HLLI
    hlli_val = hlli.get("hlli")
    if hlli_val is not None:
        if hlli_val > 0.3:
            scores.append(("HLLI", 2))
        elif hlli_val > 0:
            scores.append(("HLLI", 1))
        elif hlli_val > -0.3:
            scores.append(("HLLI", -1))
        else:
            scores.append(("HLLI", -2))

    # McClellan
    mco = mcclellan.get("mcclellan_oscillator")
    if mco is not None:
        if mco > 0.03:
            scores.append(("McClellan", 1))
        elif mco > -0.03:
            scores.append(("McClellan", 0))
        else:
            scores.append(("McClellan", -1))

    # Breakeven inflation
    be10 = fred.get("breakeven_10y")
    if be10 is not None:
        if 2.0 <= be10 <= 2.5:
            scores.append(("Breakeven", 1))  # anchored
        elif be10 < 1.5 or be10 > 3.0:
            scores.append(("Breakeven", -2))  # extreme
        else:
            scores.append(("Breakeven", 0))

    # Dollar
    # (Dollar is contextual — strong dollar is bad for EM/commodities but can be risk-off signal)

    # ── Composite ─────────────────────────────────────────────────────────
    total_score = sum(s for _, s in scores)
    max_possible = len(scores) * 2
    min_possible = -max_possible

    if max_possible > 0:
        normalized = total_score / max_possible  # -1 to +1
    else:
        normalized = 0

    if normalized > 0.4:
        regime = "RISK-ON (bullish macro backdrop)"
    elif normalized > 0.1:
        regime = "LEAN RISK-ON (cautiously bullish)"
    elif normalized > -0.1:
        regime = "NEUTRAL (mixed signals)"
    elif normalized > -0.4:
        regime = "LEAN RISK-OFF (cautiously bearish)"
    else:
        regime = "RISK-OFF (defensive positioning warranted)"

    return {
        "composite_score": total_score,
        "max_possible_score": max_possible,
        "normalized_score": round(normalized, 3),
        "regime": regime,
        "indicator_scores": {name: score for name, score in scores},
        "bullish_factors": [name for name, s in scores if s > 0],
        "bearish_factors": [name for name, s in scores if s < 0],
        "neutral_factors": [name for name, s in scores if s == 0],
    }
