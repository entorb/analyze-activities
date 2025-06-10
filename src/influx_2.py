"""Read the InfluxDB Shelly data and convert it to JSON."""

import csv
import datetime as dt
from pathlib import Path

import pandas as pd

from helper import append_data

FILE_IN = Path("data/influx.csv")
WATT_IDLE = 50
WATT_GAMING_3D_MIN = 450
WATT_MOVIE = 207
WATT_MOVIE_DELTA = 30

# gaming 3D: 450W
# movie: 207W
# PC, non gaming?
# gaming 2D?


def main_influx_v1(file_in: Path) -> dict[str, list[str]]:
    """Read influx.csv and return dict."""
    db: dict[str, list[str]] = {}
    with file_in.open(mode="r", encoding="utf-8") as fh:
        csv_reader = csv.DictReader(fh, delimiter="\t")
        for row in csv_reader:
            # 2025-06-03 17:05:00
            my_dt = dt.datetime.fromisoformat(row["datetime"])
            date = str(my_dt.date())
            time = my_dt.strftime("%H:%M")
            s = time
            append_data(db, date, s)
    return db


def main_influx_v2(file_in: Path) -> pd.DataFrame:
    """
    Read influx.csv and return df.

    returning datetime as index and column watt_last only
    """
    df = pd.read_csv(file_in, sep="\t", usecols=["datetime", "watt_now"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime")
    df = df.rename(columns={"watt_now": "watt"})
    return df


if __name__ == "__main__":
    # db = main_influx_v1(FILE_IN)
    # print(db)
    # export_json(db=db, filename="rtm")
    df = main_influx_v2(FILE_IN)

    # gaming
    df.loc[df["watt"] >= WATT_GAMING_3D_MIN, "activity"] = "gaming"

    # movie
    df.loc[
        (df["watt"] >= WATT_MOVIE - WATT_MOVIE_DELTA)
        & (df["watt"] <= WATT_MOVIE + WATT_MOVIE_DELTA),
        "activity",
    ] = "movie"

    # idle
    df.loc[df["watt"] <= WATT_IDLE, "activity"] = "idle"

    # fill missing values by "unknown"
    df["activity"] = df["activity"].fillna("unknown")

    # remove where activity is idle
    # df = df[df["activity"] != "idle"]

    # Identify where activity changes
    df["activity_change"] = (
        (df["activity"] != df["activity"].shift()).astype(int).cumsum()
    )

    # Group by activity_change to get segments
    grouped = df.groupby("activity_change")

    records = []
    for _, group in grouped:
        activity = group["activity"].iloc[0]
        start_time = group.index[0]
        duration = (
            group.index[-1] - group.index[0]
        ).total_seconds() / 60 + 1  # minutes, +1 to include both endpoints
        records.append(
            {"start": start_time, "activity": activity, "duration": int(duration)}
        )

    df2 = pd.DataFrame(records).set_index("start")

    print(df2.tail(50))
