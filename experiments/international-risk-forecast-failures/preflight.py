#!/usr/bin/env python3
"""Stage-0 input audit for the proposed international risk study.

Does NOT fit a DFM, estimate smoothing, run a backtest, or establish
point-in-time validity beyond the supplied availability-date checks.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date
import json
import math
from pathlib import Path
import sys

REQUIRED = ("country", "observation_date", "available_date", "variable", "value", "source")


def audit_panel(path: str | Path) -> dict:
    path = Path(path)
    counts = Counter()
    spans = defaultdict(list)
    unique = set()
    errors = []
    total = 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [name for name in REQUIRED if name not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(missing))
        for line_no, row in enumerate(reader, start=2):
            total += 1
            try:
                country = (row["country"] or "").strip().upper()
                variable = (row["variable"] or "").strip().lower()
                source = (row["source"] or "").strip()
                if not (country and variable and source):
                    raise ValueError("country, variable and source must be non-empty")
                observed = date.fromisoformat((row["observation_date"] or "").strip())
                available = date.fromisoformat((row["available_date"] or "").strip())
                if available < observed:
                    raise ValueError("available_date is earlier than observation_date")
                value = float(row["value"])
                if not math.isfinite(value):
                    raise ValueError("value must be finite")
                key = (country, observed.isoformat(), variable)
                if key in unique:
                    raise ValueError("duplicate country/observation_date/variable")
                unique.add(key)
                pair = (country, variable)
                counts[pair] += 1
                spans[pair].append(observed.isoformat())
            except (ValueError, TypeError, KeyError) as exc:
                errors.append({"line": line_no, "error": str(exc)})
    if total == 0:
        errors.append({"line": 1, "error": "no observations"})
    return {
        "status": "PASS" if not errors else "FAIL",
        "input": str(path),
        "total_rows": total,
        "valid_rows": sum(counts.values()),
        "errors": errors,
        "series": [
            {
                "country": country,
                "variable": variable,
                "n_observations": counts[(country, variable)],
                "first_observation": min(spans[(country, variable)]),
                "last_observation": max(spans[(country, variable)]),
            }
            for country, variable in sorted(counts)
        ],
        "limitations": [
            "Release dates are user-supplied and have not been externally verified.",
            "PASS does not prove data were available to historical forecasters.",
            "No model was estimated or evaluated.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Long-form indicator CSV")
    parser.add_argument("--report", help="Optional path to save the JSON audit")
    args = parser.parse_args()
    try:
        result = audit_panel(args.input)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, indent=2))
        return 2
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.report:
        output = Path(args.report)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
