"""Tests for cal.py."""
# ruff: noqa: D103 PLR2004 INP001 DTZ001

import datetime as dt
import zoneinfo
from pathlib import Path

from cal import TZ_DE, convert_date_or_dt_to_dt, main


def test_convert_date_to_dt() -> None:
    date = dt.date(2024, 6, 1)
    result = convert_date_or_dt_to_dt(date)
    assert isinstance(result, dt.datetime)
    assert result == dt.datetime(2024, 6, 1, 0, 0, 0)


def test_convert_naive_datetime_to_dt() -> None:
    naive_dt = dt.datetime(2024, 6, 1, 15, 30, 45, 123456)
    result = convert_date_or_dt_to_dt(naive_dt)
    assert isinstance(result, dt.datetime)
    assert result == dt.datetime(2024, 6, 1, 15, 30, 45)


def test_convert_aware_datetime_to_dt() -> None:
    aware_dt = dt.datetime(2024, 6, 1, 15, 30, 0, tzinfo=TZ_DE)
    result = convert_date_or_dt_to_dt(aware_dt)
    assert isinstance(result, dt.datetime)
    # Should be the same time, but tzinfo removed
    assert result == dt.datetime(2024, 6, 1, 15, 30, 0)
    assert result.tzinfo is None


def test_convert_utc_aware_datetime_to_dt() -> None:
    utc = zoneinfo.ZoneInfo("UTC")
    aware_dt = dt.datetime(2024, 6, 1, 13, 30, 0, tzinfo=utc)
    result = convert_date_or_dt_to_dt(aware_dt)
    # 13:30 UTC == 15:30 Europe/Berlin in summer
    assert result == dt.datetime(2024, 6, 1, 15, 30, 0)
    assert result.tzinfo is None


def test_main() -> None:
    db = main(p=Path("tests/testdata/cal.ics"))
    assert db["2009-10-18"] == ["00:00 Title Full Day"]
    assert "2023-06-15" not in db  # repeating
    assert db["2025-05-31"] == ["14:00 Title 1", "14:30 Title 2"]


test_main()
