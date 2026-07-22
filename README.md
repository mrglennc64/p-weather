# Weather near-resolution lag-logger

A **read-only measurement instrument** for Polymarket weather markets. Not a
trading bot and not a pick-seller — it places no orders, holds no wallet, and
uses no API keys. It answers one question with evidence:

> When a weather market becomes **mechanically decided** by the temperature
> that has *already been observed*, how long does the market price take to
> catch up — and how many dollars are actually fillable in that gap?

## The idea: a fact, not a forecast

Polymarket runs markets like *"Highest temperature in Beijing on July 22?"*
with buckets (`73–74°C`, `75°C or above`, …). Each settles on the highest
temperature recorded that day at **one specific airport weather station**
(via Wunderground). A daily maximum can only rise — so the moment the
station's observed high clears a bucket boundary, that bucket's outcome is
**settled in advance**:

- **PROVEN** — the station already reached an *"X or above"* floor → resolves YES, forever.
- **DEAD** — the station already exceeded a bucket's ceiling → resolves NO, forever.

The tool flags **only** these already-happened facts. *"The peak has probably
passed"* is still a forecast and is deliberately never counted. A safety
margin (1 °F / 0.5 °C) absorbs rounding differences between the raw station
report and Wunderground's published figure.

This is the Polymarket analog of a live-betting trigger: not out-predicting
the crowd, but reading the *settlement instrument itself* faster than the
market updates.

## How it works

| Module | Job |
|---|---|
| `rules` | Parse each market's own rules → settlement station (ICAO), unit, source. Self-configuring; unidentifiable markets are EXCLUDED. |
| `metar` | Observed daily max from the station's METARs (`aviationweather.gov`, free, global). |
| `localtime` | DST-correct local-day boundary (offset from Open-Meteo). |
| `lock` | PROVEN / DEAD / still-live, with the safety margin. |
| `clob` | Public order-book depth → **fillable edge-dollars** (the headline metric). |
| `fetch` | Live weather markets from the Polymarket Gamma API. |
| `scan` | One poll: detect → snapshot depth → append `LOCK`/`SNAPSHOT`/`CONCEDE`. |
| `digest` | Per-city verdict lines + an honest global ceiling. |
| `db` | Standalone append-only `trigger_events` table. |

The lag between a `LOCK` and its `CONCEDE` (price finally crossing 0.95/0.05)
**is the measurement**.

## Data sources (all free, no key)

- **Polymarket Gamma API** — market metadata, prices, token ids
- **Polymarket CLOB `/book`** — order-book depth (read-only)
- **aviationweather.gov** — global METAR observations
- **Open-Meteo** — DST-correct UTC offset per station

## Usage

```bash
pip install -r requirements.txt

python scan.py test        # unit tests (no network)
python scan.py rules       # write exports/weather_rules_review.md — REVIEW FIRST
python scan.py once        # one read-only scan pass
python scan.py watch 1440  # continuous 24h watch loop (adaptive 5/10-min poll)
python scan.py digest      # per-city verdicts from the log
```

Data lands in an append-only SQLite table (`weather.sqlite` by default; set
`WEATHER_DB` to change). Review `exports/weather_rules_review.md` before
trusting any market — it is the acceptance gate that catches misparsed units,
missing stations, and non-airport settlement sources (e.g. Hong Kong resolves
on the Hong Kong Observatory, not a METAR — correctly excluded).

## Honest status

The instrument is built and validated (mechanics cross-checked against raw
station data). But an edge is **not proven**: a single snapshot can't show
whether prices actually concede, the deep-in-the-money buckets are already
priced correctly, and the dollars concentrate on knife-edge buckets carrying
the most rounding/revision risk. **Run it for several days to measure real
concede-lag, and hand-audit a sample of locks against Wunderground before
believing any dollar figure.** See `docs/weather-trigger-explained.pdf`.

Extracted as a standalone project from the Contest Edge prediction app.
