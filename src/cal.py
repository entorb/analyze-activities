"""
Read calendar appointments and convert to json list.

based on https://github.com/entorb/tools-calendar/blob/main/upcoming_events.py
"""

import datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo

import icalendar

from helper import append_data, export_json

TZ_DE = ZoneInfo("Europe/Berlin")
FILE_IN = Path("data/cal/cal-torben-nc.ics")
TODAY = dt.datetime.now(tz=TZ_DE).date()
NOW_DT = dt.datetime.now(tz=TZ_DE).replace(tzinfo=None)


def convert_date_or_dt_to_dt(date_or_dt: dt.date | dt.datetime) -> dt.datetime:
    """
    Convert date or datetime to datetime.

    in German timezone, without timezone info
    """
    if type(date_or_dt) is dt.datetime:
        my_dt = date_or_dt.replace(microsecond=0)
        if my_dt.tzinfo is not None:
            my_dt = my_dt.astimezone(TZ_DE).replace(tzinfo=None)
    else:
        my_dt = dt.datetime.combine(date_or_dt, dt.time(0, 0, 0), tzinfo=None)
    return my_dt


def main(p: Path) -> dict[str, list[str]]:  # noqa: D103
    db: dict[str, list[str]] = {}

    with p.open(encoding="utf-8", newline="\r\n") as f:
        calendar = icalendar.Calendar.from_ical(f.read())

    for event in calendar.walk("VEVENT"):
        title = str(event.get("SUMMARY")).strip()
        if Path("src/name_fix.py").exists():
            from name_fix import name_fix

            title = name_fix(title)

        # Skip repeating events
        if "RRULE" in event:
            # print("skipping", title)
            continue

        start = event.get("DTSTART").dt

        # skip future events
        if (type(start) is dt.date and start > TODAY) or (
            type(start) is dt.datetime and start.replace(tzinfo=None) > NOW_DT
        ):
            continue

        # TODO: how to handle multi day events

        # full-day events
        if type(start) is dt.date:
            date = str(start)
            s = f"00:00 {title}"
        else:
            my_dt = convert_date_or_dt_to_dt(start)
            date = str(my_dt.date())
            s = f"{my_dt.strftime('%H:%M')} {title}"

        append_data(db, date, s)
    return db


if __name__ == "__main__":
    db = main(p=FILE_IN)
    export_json(db=db, filename="cal")
