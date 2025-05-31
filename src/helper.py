"""Helper functions."""

import json
from pathlib import Path


def export_json(db: dict[str, list[str]], filename: str) -> None:
    """Export sorted data as json."""
    # sorting
    db2: dict[str, list[str]] = {}
    for key in sorted(db.keys()):
        lst = sorted(db[key])
        db2[key] = lst

    # export to json
    with Path(f"data/{filename}.json").open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(db2, fh, ensure_ascii=False, sort_keys=False, indent=2)


def append_data(db: dict[str, list[str]], date: str, s: str) -> None:
    """Append data to date."""
    if date in db:
        db[date].append(s)
    else:
        db[date] = [s]
