"""Summarize synthetic shift production data from CSV."""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

REQUIRED = {"date", "shift", "planned_tonnes", "actual_tonnes", "scheduled_minutes", "downtime_minutes", "cycle_time_min", "material"}


def parse_rows(path):
    valid, rejected = [], 0
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError("CSV does not contain all required columns")
        for row in reader:
            try:
                planned, actual = float(row["planned_tonnes"]), float(row["actual_tonnes"])
                scheduled, downtime = float(row["scheduled_minutes"]), float(row["downtime_minutes"])
                cycle = float(row["cycle_time_min"])
                if planned <= 0 or actual < 0 or scheduled <= 0 or not 0 <= downtime <= scheduled or cycle < 0:
                    raise ValueError()
                valid.append({**row, "planned_tonnes": planned, "actual_tonnes": actual,
                              "scheduled_minutes": scheduled, "downtime_minutes": downtime,
                              "cycle_time_min": cycle})
            except (ValueError, TypeError, KeyError): rejected += 1
    return valid, rejected


def analyze(rows, rejected, source):
    groups = defaultdict(list)
    for row in rows: groups[row["shift"]].append(row)
    summaries = {}
    for shift, values in sorted(groups.items()):
        actual = sum(x["actual_tonnes"] for x in values)
        plan = sum(x["planned_tonnes"] for x in values)
        scheduled = sum(x["scheduled_minutes"] for x in values)
        operating = sum(x["scheduled_minutes"] - x["downtime_minutes"] for x in values)
        summaries[shift] = {
            "records": len(values), "actual_tonnes": round(actual, 1), "planned_tonnes": round(plan, 1),
            "compliance_pct": round(100 * actual / plan, 1),
            "availability_pct": round(100 * operating / scheduled, 1),
            "mean_cycle_time_min": round(sum(x["cycle_time_min"] for x in values) / len(values), 2),
        }
    return {"data_kind": "synthetic_example", "source_file": source,
            "rows_valid": len(rows), "rows_rejected": rejected,
            "formulae": {"compliance": "sum(actual_tonnes) / sum(planned_tonnes) * 100",
                         "availability": "sum(scheduled_minutes - downtime_minutes) / sum(scheduled_minutes) * 100",
                         "mean_cycle_time": "mean(cycle_time_min)"},
            "by_shift": summaries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("report.json"))
    args = parser.parse_args()
    try:
        rows, rejected = parse_rows(args.input)
        report = analyze(rows, rejected, args.input.name)
    except (OSError, ValueError) as exc: parser.error(str(exc))
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__": main()
