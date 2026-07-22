"""Weather near-resolution lag-logger — strictly read-only, paper-mode.

Measures, for each Polymarket "Highest temperature in <city> on <date>?"
market, the lag between a bucket becoming MECHANICALLY DECIDED by the
observed station temperature and the market price catching up — plus the
dollars fillable in that gap. No orders, no wallet, no API keys.

Extracted as a standalone project from Contest Edge. Modules:
  rules      parse each market's own settlement rules (ICAO station, unit)
  metar      observed daily max from the settlement station's METARs
  localtime  DST-correct local-day boundary
  lock       PROVEN/DEAD detector (already-exceeded facts only)
  clob       order-book depth + fillable edge-dollars
  fetch      live weather markets from the Polymarket Gamma API
  buckets    bucket-label -> numeric bounds
  scan       one poll: detect, snapshot, append to trigger_events
  digest     per-city verdict lines
  db         standalone append-only trigger_events table
"""
