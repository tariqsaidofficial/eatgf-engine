import json
from dataclasses import asdict

def serialize_report(report, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            asdict(report),
            f,
            indent=2,
            sort_keys=True
        )
