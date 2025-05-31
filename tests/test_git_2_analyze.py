"""Tests for git."""

# ruff: noqa: D103 PLR2004 INP001

from pathlib import Path

from git_2_analyze import extract_data_from_log_entry, process_file


def test_extract_data_from_log_entry_1() -> None:
    element = """2025-01-07T21:37:10+01:00: Update .gitattributes
 1 file changed, 1 insertion(+), 26 deletions(-)
"""
    d = extract_data_from_log_entry(element)
    assert d["date"] == "2025-01-07", d["date"]
    assert d["time"] == "21:37", d["time"]
    assert d["title"] == "Update .gitattributes", d["title"]
    assert d["files"] == 1, d["files"]
    assert d["insert"] == 1, d["insert"]
    assert d["del"] == 26, d["del"]


def test_extract_data_from_log_entry_2() -> None:
    element = """2024-07-13T07:18:11+02:00: Fixing Ruff
 10 files changed, 140 insertions(+), 113 deletions(-)
"""
    d = extract_data_from_log_entry(element)
    assert d["date"] == "2024-07-13", d["date"]
    assert d["time"] == "07:18", d["time"]
    assert d["title"] == "Fixing Ruff", d["title"]
    assert d["files"] == 10, d["files"]
    assert d["insert"] == 140, d["insert"]
    assert d["del"] == 113, d["del"]


def test_extract_data_from_log_entry_3() -> None:
    element = """2024-07-13T03:25:16+02:00: convert json transactions to excel
 2 files changed, 87 insertions(+)
"""
    d = extract_data_from_log_entry(element)
    assert d["date"] == "2024-07-13", d["date"]
    assert d["time"] == "03:25", d["time"]
    assert d["title"] == "convert json transactions to excel", d["title"]
    assert d["files"] == 2, d["files"]
    assert d["insert"] == 87, d["insert"]
    assert d["del"] == 0, d["del"]


def test_process_file() -> None:
    db: dict[str, list[str]] = {}
    process_file(p=Path("tests/testdata/git.log"), db=db)
    print(db)
    assert db["2021-05-13"] == [
        "19:21 Coding at git: Update README.md (8 changes)",
        "19:10 Coding at git: Initial commit (17770 changes)",
    ]
    assert db["2021-05-27"] == ["11:35 Coding at git: added disputation (1549 changes)"]
