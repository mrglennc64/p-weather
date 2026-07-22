"""Weather near-resolution lag-logger — CLI.

  python scan.py test              # unit tests (no network)
  python scan.py rules             # write exports/weather_rules_review.md
  python scan.py once              # one read-only scan pass
  python scan.py watch [minutes]   # continuous watch loop (default 720)
  python scan.py digest            # per-city verdict lines from the log

Strictly read-only against Polymarket: no orders, no wallet, no keys.
"""
import sys


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "test":
        from weather_trigger import tests
        tests.main()
    elif cmd == "rules":
        from weather_trigger import review
        review.main()
    elif cmd == "once":
        from weather_trigger import scan, db
        scan.scan_once(db.init_db(), verbose=True)
    elif cmd == "watch":
        from weather_trigger import scan
        scan.run(int(sys.argv[2]) if len(sys.argv) > 2 else 720)
    elif cmd == "digest":
        from weather_trigger import digest
        digest.print_digest()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
