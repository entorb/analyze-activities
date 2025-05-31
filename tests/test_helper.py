"""Tests for helper.py."""
# ruff: noqa: D103 PLR2004 INP001 DTZ001

from helper import append_data


def test_append_data_adds_to_existing_date() -> None:
    db: dict[str, list[str]] = {"2024-01-01": ["foo"]}
    append_data(db, "2024-01-01", "bar")
    assert db == {"2024-01-01": ["foo", "bar"]}


def test_append_data_creates_new_date() -> None:
    db: dict[str, list[str]] = {}
    append_data(db, "2024-06-01", "baz")
    assert db == {"2024-06-01": ["baz"]}


def test_append_data_multiple_calls() -> None:
    db: dict[str, list[str]] = {}
    append_data(db, "2024-06-01", "a")
    append_data(db, "2024-06-01", "b")
    append_data(db, "2024-06-02", "c")
    assert db == {"2024-06-01": ["a", "b"], "2024-06-02": ["c"]}


def test_append_data_with_empty_string() -> None:
    db: dict[str, list[str]] = {"2024-01-01": []}
    append_data(db, "2024-01-01", "")
    assert db == {"2024-01-01": [""]}
