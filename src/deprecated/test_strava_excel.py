"""Tests for strava.py."""

# ruff: noqa: D103 PLR2004 INP001

import pandas as pd

from deprecated.strava_excel import cleanup


def test_cleanup_basic() -> None:
    df = pd.DataFrame(
        {
            "x_date": ["2024-06-01"],
            "start_date_local": ["2024-06-01 07:30:00"],
            "name": ["123/365 Morning Ride"],
            "type": ["Ride"],
            "x_min": [45.4],
        }
    )
    result = cleanup(df)
    assert list(result.columns) == ["date", "s"]
    assert result.iloc[0]["date"] == "2024-06-01"
    assert result.iloc[0]["s"].startswith("07:30 Cycling: Morning Ride (45 min)")  # type: ignore


def test_cleanup_run_and_title_strip() -> None:
    df = pd.DataFrame(
        {
            "x_date": ["2024-06-02"],
            "start_date_local": ["2024-06-02 18:15:00"],
            "name": ["42/365 Evening Run "],
            "type": ["Run"],
            "x_min": [30.7],
        }
    )
    result = cleanup(df)
    assert "Jogging" in result.iloc[0]["s"]
    assert "Evening Run" in result.iloc[0]["s"]
    assert "42/365" not in result.iloc[0]["s"]


def test_cleanup_minutes_rounding() -> None:
    df = pd.DataFrame(
        {
            "x_date": ["2024-06-03"],
            "start_date_local": ["2024-06-03 12:00:00"],
            "name": ["Midday Ride"],
            "type": ["Ride"],
            "x_min": [29.6],
        }
    )
    result = cleanup(df)
    assert "(30 min)" in result.iloc[0]["s"]


def test_cleanup_multiple_rows() -> None:
    df = pd.DataFrame(
        {
            "x_date": ["2024-06-04", "2024-06-05"],
            "start_date_local": ["2024-06-04 09:00:00", "2024-06-05 10:30:00"],
            "name": ["Morning Ride", "Afternoon Run"],
            "type": ["Ride", "Run"],
            "x_min": [60, 25],
        }
    )
    result = cleanup(df)
    assert len(result) == 2
    assert "Cycling" in result.iloc[0]["s"]
    assert "Jogging" in result.iloc[1]["s"]
