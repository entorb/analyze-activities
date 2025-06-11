"""Read the InfluxDB Shelly data and convert it to JSON."""

from pathlib import Path

import pandas as pd

from helper import append_data, export_json

FILE_IN = Path("data/influx-media.csv")
DURATION_MIN = 10


def read_data_df(file_in: Path) -> pd.DataFrame:
    """
    Read influx.csv and return df.

    returning datetime as index and column watt_last only
    """
    df = pd.read_csv(file_in, sep="\t", usecols=["datetime", "watt_now"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime")
    df = df.rename(columns={"watt_now": "watt"})
    return df


def guess_activity(watt: float) -> str:
    """Guess activity based on watt."""
    # gaming 3D: 450W
    # movie: 207W
    # PC, non gaming?
    # gaming 2D?

    if watt <= 50:  # noqa: PLR2004
        return "idle"
    if watt >= 450:  # noqa: PLR2004
        return "gaming"
    if watt >= 207 - 30 and watt <= 207 + 30:
        return "movie"
    return "unknown"


def df_grouping_to_dict(df: pd.DataFrame) -> dict[str, list[str]]:
    """Derive activities from raw data and calc length."""
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

    # remove where activity is idle
    df2 = df2[df2["activity"] != "idle"]
    df2 = df2[df2["activity"] != "unknown"]
    df2 = df2[df2["duration"] > DURATION_MIN]
    # print(df2.tail(50))

    db: dict[str, list[str]] = {}
    for row in df2.itertuples():
        date = str(row.Index.date())  # type: ignore
        s = f"Media: {row.activity} ({row.duration} min)"  # TODO: add time
        append_data(db, date, s)
    return db


if __name__ == "__main__":
    df = read_data_df(FILE_IN)
    db = df_grouping_to_dict(df)
    export_json(db=db, filename=FILE_IN.stem)
