"""Tests for Journal."""

# ruff: noqa: D103 PLR2004 INP001

from pathlib import Path

from journal import main_journal


def test_journal() -> None:
    db = main_journal(Path("tests/testdata/journal.md"))
    # cspell:disable
    assert db == {
        "2025-05-19": ["07:00 aufgestanden", "08:00 Rad ins Büro"],
        "2025-05-20": [
            "Hier ein Beispiel für einen gemixten Tag",
            "12:00 Mittagessen",
            "Früh ins Bett",
        ],
    }
    # cspell:enable
