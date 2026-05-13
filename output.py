import csv
import json


def save_report(results, target, filepath, format):
    if format == "json":
        save_json(results, target, filepath)
    elif format == "csv":
        save_csv(results, filepath)


def save_json(results, target, filepath):
    report = {
        "target": target,
        "results": [
            {"port": port, "status": status} for port, status in sorted(results.items())
        ],
    }

    with open(filepath, "w") as f:
        json.dump(report, f, indent=4)
    print(f"\n Report  saved to {filepath}")


def save_csv(results, filepath):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["port", "status"])
        for port, status in sorted(results.items()):
            writer.writerow([port, status])
    print(f"\n Report saved to {filepath}")
