"""Bucket-label parser (extracted from the Contest Edge weather lane).

Turns a Polymarket temperature bucket label into numeric [lo, hi] bounds:
  '73-74°F'       -> (72.5, 74.5)
  '75°F or above' -> (74.5, inf)
  '72°F or below' -> (-inf, 72.5)
  '26°C'          -> (25.5, 26.5)   (single-degree bucket)
hi may be math.inf, lo may be -math.inf.
"""
import math
import re

_RANGE = re.compile(r"(\d+)\s*[-–]\s*(\d+)")
_ABOVE = re.compile(r"(\d+)\s*°?\s*[FC]?\s*(?:or above|or higher|\+)", re.I)
_BELOW = re.compile(r"(\d+)\s*°?\s*[FC]?\s*(?:or below|or lower|or less)", re.I)


def _bucket(text: str):
    m = _RANGE.search(text)
    if m:
        return float(m.group(1)) - 0.5, float(m.group(2)) + 0.5
    m = _ABOVE.search(text)
    if m:
        return float(m.group(1)) - 0.5, math.inf
    m = _BELOW.search(text)
    if m:
        return -math.inf, float(m.group(1)) + 0.5
    m = re.fullmatch(r"\s*(\d+)\s*°?\s*[FC]?\s*", text)   # single-degree
    if m:                                                  # bucket: '26°C'
        n = float(m.group(1))
        return n - 0.5, n + 0.5
    return None
