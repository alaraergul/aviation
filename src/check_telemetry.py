from pathlib import Path
import pandas as pd

project = Path(__file__).resolve().parent.parent
file_path = project / "data" / "selected_flight.csv"

df = pd.read_csv(file_path)

df["datetime"] = pd.to_datetime(
    df["time"], unit="s", utc=True
)

df["position_age"] = df["time"] - df["lastposupdate"]

periods = [
    ("12:07:30", "12:09:30"),
    ("12:16:30", "12:19:00")
]

columns = [
    "datetime",
    "baroaltitude",
    "velocity",
    "vertrate",
    "onground",
    "position_age"
]

for start, end in periods:
    start_time = pd.Timestamp(
        f"2019-01-07 {start}", tz="UTC"
    )
    end_time = pd.Timestamp(
        f"2019-01-07 {end}", tz="UTC"
    )

    selected = df[
        (df["datetime"] >= start_time) &
        (df["datetime"] <= end_time)
    ]

    print(f"\n--- {start} to {end} UTC ---")
    print(selected[columns].to_string(index=False))

print("\nPosition age summary:")
print(df["position_age"].describe())

print("\nOn-ground values:")
print(df["onground"].value_counts(dropna=False))