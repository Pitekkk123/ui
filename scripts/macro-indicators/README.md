# Macro Indicators Snapshot

Skrypt Python zbierający **19 klas wskaźników makro/sentymentu** z darmowych źródeł i generujący JSON snapshot z analizą sygnałów.

## Źródła danych

| Warstwa | Źródło | Limit | Wskaźniki |
|---------|--------|-------|-----------|
| Makro/kredyt/yieldy | FRED API | Unlimited | HY OAS, IG OAS, NFCI, ANFCI, yieldy (3M/2Y/10Y/30Y), spready (2s10s, 3M10Y), TIPS, breakeveny, DXY, VIX |
| VIX/VVIX | CBOE CDN | Unlimited CSV | VIX, VVIX, VX futures term structure |
| GEX | yfinance | Unlimited | Gamma Exposure z opcji SPY |
| Options Flow | yfinance | Unlimited | P/C ratios: TLT, SQQQ, UVXY, VXX, SDS |
| MOVE proxy | yfinance | Unlimited | TLT 20d realized vol |
| Breadth | Stooq | Unlimited | TRIN, HLLI, McClellan Oscillator & Summation |

## Instalacja

```bash
cd scripts/macro-indicators
pip install -r requirements.txt
```

## Konfiguracja

1. Zarejestruj darmowy klucz FRED API: https://fred.stlouisfed.org/docs/api/api_key.html
2. Ustaw zmienną środowiskową:

```bash
export FRED_API_KEY="twoj_klucz_tutaj"
```

## Użycie

```bash
# Jednorazowy snapshot:
python macro_snapshot.py

# Tryb szybki (pomija GEX i options flow):
python macro_snapshot.py --fast

# Tylko wydruk do konsoli:
python macro_snapshot.py --print-only

# Scheduler — uruchom codziennie o 20:00:
python macro_snapshot.py --schedule

# Zmień czas schedulera:
MACRO_RUN_TIME=18:30 python macro_snapshot.py --schedule

# Własny katalog wyjściowy:
python macro_snapshot.py -o /path/to/output

# Debug logging:
python macro_snapshot.py -v
```

## Output

- `macro_snapshot.json` — najnowszy snapshot
- `macro_history.json` — historia (max 365 wpisów)

### Struktura JSON

```json
{
  "meta": { "timestamp_utc": "...", "version": "1.0.0" },
  "fred": { "hy_oas": 3.45, "spread_2s10s": -0.12, ... },
  "cboe_vix_vvix": { "vix": 18.5, "vvix": 95.2, "vix_zone": "15-22" },
  "cboe_vx_futures": { "vx1": 19.5, "vx2": 21.0, "vx_ratio": 0.93 },
  "gex": { "gex_total_billions": 2.45, "gex_signal": "positive" },
  "options_flow": { "TLT": { "pc_ratio": 1.6 }, ... },
  "move_proxy": { "tlt_realized_vol_20d": 14.5 },
  "trin": { "trin": 1.05, "trin_signal": "neutral" },
  "hlli": { "hlli": 0.35, "hlli_signal": "moderate bullish" },
  "mcclellan": { "mcclellan_oscillator": 0.02 },
  "analysis": {
    "credit_stress": { ... },
    "yield_curve": { ... },
    "composite": {
      "normalized_score": 0.25,
      "regime": "LEAN RISK-ON"
    }
  }
}
```

## Composite Signal

Skrypt generuje złożony sygnał risk-on/risk-off na podstawie wszystkich wskaźników:

| Score | Reżim |
|-------|-------|
| > 0.4 | RISK-ON |
| 0.1 — 0.4 | LEAN RISK-ON |
| -0.1 — 0.1 | NEUTRAL |
| -0.4 — -0.1 | LEAN RISK-OFF |
| < -0.4 | RISK-OFF |

## Ograniczenia

- **MOVE Index** — prawdziwy ICE BofA MOVE wymaga płatnej subskrypcji. Używamy TLT realized vol jako proxy.
- **GEX** — przybliżenie z opcji SPY, nie pełny dealer gamma z SqueezeMetrics.
- **Dark pool flow** — niedostępny za darmo.
- **McClellan** — zależy od dostępności danych breadth na Stooq.
