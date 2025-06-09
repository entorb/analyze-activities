"""Read the Remember the Milk task list and convert to JSON."""

import csv
from pathlib import Path

from helper import append_data, export_json

FILE_IN = Path("data/rtm_tasks_completed.csv")
MIN_TASK_ESTIMATION = 5


def main_rtm(file_in: Path) -> dict[str, list[str]]:
    """Read rtm_tasks_completed.csv and return dict."""
    db: dict[str, list[str]] = {}
    with file_in.open(mode="r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh, delimiter="\t")
        for row in csv_reader:
            if row["estimate"] != "" and int(row["estimate"]) <= MIN_TASK_ESTIMATION:
                continue

            if "Oura Ring laden" in row["name"]:
                continue
            date = row["completed"]
            s = f"{row['completed_time']} Task {row['list']}: {row['name']} ({row['estimate']}min)"  # noqa: E501
            append_data(db, date, s)

    return db


if __name__ == "__main__":
    db = main_rtm(FILE_IN)
    export_json(db=db, filename="rtm")
