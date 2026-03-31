
import csv
from typing import Dict, List


def normalize_title(title: str) -> str:
    return str(title).strip().lower()


def detect_title_field(fieldnames: List[str]) -> str:
    preferred = ["track_name", "title", "song_title", "name"]
    lowered = {f.lower(): f for f in fieldnames}
    for candidate in preferred:
        if candidate in lowered:
            return lowered[candidate]
    # fallback: first column that looks title-like
    for name in fieldnames:
        if "title" in name.lower() or "track" in name.lower() or "name" == name.lower():
            return name
    raise ValueError("Could not identify a title column in the dataset.")


def load_csv_records(csv_path: str) -> List[Dict[str, str]]:
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        records = list(reader)
        if not records:
            return []
        title_field = detect_title_field(reader.fieldnames or [])
        for record in records:
            record["_title_field"] = title_field
        return records


def record_title(record: Dict[str, str]) -> str:
    return record.get(record["_title_field"], "")


def comparable_records(records: List[Dict[str, str]]) -> List[tuple]:
    cleaned = []
    for r in records:
        cleaned.append(tuple(sorted((k, v) for k, v in r.items() if k != "_title_field")))
    return sorted(cleaned)
