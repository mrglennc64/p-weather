"""Standalone ledger — one append-only table.

Extracted from Contest Edge's six-table ledger; this project keeps only the
trigger_events log. APPEND-ONLY: no UPDATE statement for it exists anywhere.
Set WEATHER_DB to point elsewhere (default: ./weather.sqlite).
"""
import os

from sqlalchemy import (Column, Float, Integer, MetaData, Table, Text,
                        create_engine)

DB_URL = os.environ.get("WEATHER_DB", "sqlite:///weather.sqlite")
metadata = MetaData()

trigger_events = Table(                                # APPEND-ONLY snapshot log
    "trigger_events", metadata,                        # one row per poll per locked
    Column("id", Integer, primary_key=True, autoincrement=True),  # bucket; timeline
    Column("mslug", Text, nullable=False),             # is the ordered sequence
    Column("city", Text, nullable=False),
    Column("icao", Text, nullable=False),              # settlement station
    Column("side", Text, nullable=False),              # the bucket label
    Column("state", Text, nullable=False),             # PROVEN | DEAD
    Column("kind", Text, nullable=False),              # LOCK | SNAPSHOT | CONCEDE
    Column("boundary", Float, nullable=False),
    Column("unit", Text, nullable=False),              # celsius | fahrenheit
    Column("obs_max", Float, nullable=False),          # station max at snapshot
    Column("fair", Float, nullable=False),             # 1.0 PROVEN, 0.0 DEAD
    Column("market_p", Float, nullable=False),         # yes-price at snapshot
    Column("best_bid", Float),                         # certain side's token
    Column("best_ask", Float),
    Column("mispricing_cents", Float),                 # (fair - best_ask)*100
    Column("edge_dollars", Float),                     # fillable $ better than fair
    Column("depth_json", Text),                        # walked book at snapshot
    Column("snapshot_at", Text, nullable=False),       # UTC ISO
)


def get_engine():
    return create_engine(DB_URL)


def init_db():
    engine = get_engine()
    metadata.create_all(engine)
    return engine
