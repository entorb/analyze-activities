"""Read Strava activity Excel and convert to json list."""

from pathlib import Path

import pandas as pd

from helper import append_data, export_json

# Deprecated, better use ics export as alternative, to reduce dependency to Pandas
FILE_IN = Path("data/Strava_Activity_List.xlsx")


def cleanup(df: pd.DataFrame) -> pd.DataFrame:
    """Clean up the DataFrame."""
    df = df.rename(
        columns={
            "x_date": "date",
            "name": "title",
            "x_min": "minutes",
            "start_date_local": "time",
        }
    )

    df["minutes"] = df["minutes"].round().astype(int)

    # 2025-05-31 14:50:01 -> 14:50
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")  # type: ignore
    df["time"] = pd.to_datetime(df["time"]).dt.strftime("%H:%M")  # type: ignore

    df["type"] = df["type"].str.replace("Ride", "Cycling")  # type: ignore
    df["type"] = df["type"].str.replace("Run", "Jogging")  # type: ignore

    # title: remove leading 123/365
    df["title"] = df["title"].str.replace(r"^\d+/365\s*", "", regex=True)  # type: ignore

    df["s"] = (
        df["time"]
        + " "
        + df["type"]
        + ": "
        + df["title"]
        + " ("
        + df["minutes"].astype(str)
        + " min)"
    )
    df = df[["date", "s"]]
    return df


def main() -> None:  # noqa: D103
    df = pd.read_excel(  # type: ignore
        FILE_IN,
        usecols=["x_date", "start_date_local", "name", "type", "x_min"],
    )

    df = cleanup(df)

    db: dict[str, list[str]] = {}
    for row in df.itertuples():
        date = str(row.date)
        s = str(row.s)
        append_data(db, date, s)

    export_json(db=db, filename="strava")


if __name__ == "__main__":
    main()
