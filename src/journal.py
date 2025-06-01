"""Read my personal journal and convert to json list."""

import re
from pathlib import Path

from helper import append_data, export_json

FILE_IN = Path("data/journal/lifelog.md")

# re pattern for dates like "Do 02.01.2025"
RE_DATE_PATTERN = re.compile(r"^[A-Z][a-z] (\d{2})\.(\d{2})\.(\d{4})\s*$")

# re pattern for times without ":" like "1200"
RE_TIME_PATTERN = re.compile(r"^(\d{2})(\d{2})\b")


def main_journal(file_in: Path) -> dict[str, list[str]]:
    """Read journal.md file and return dict."""
    db: dict[str, list[str]] = {}
    with file_in.open(encoding="utf-8") as fh:
        date = "2000-01-01"
        for line in fh:
            s = line.strip()
            if s.startswith("### KW") or s == "":
                continue

            # if line is a date: "Do 02.01.2025"
            match = RE_DATE_PATTERN.match(s)
            if match:
                date = f"{match.group(3)}-{match.group(2)}-{match.group(1)}"
                continue

            # if line starts with time -> insert ":"
            match = RE_TIME_PATTERN.match(s)
            if match:
                s = f"{s[:2]}:{s[2:]}"

            if s.startswith("+T"):
                s = "super T: " + s[2:]
            if s.startswith("+"):
                s = "gut: " + s[1:]
            # replace initials by full names
            if Path("src/name_fix.py").exists():
                from name_fix import name_fix

                s = name_fix(s)

            s = s.replace("  ", " ")
            append_data(db, date, s)

    return db


if __name__ == "__main__":
    db = main_journal(FILE_IN)
    export_json(db=db, filename="journal", sort=False)
