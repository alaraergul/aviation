from pathlib import Path
import pandas as pd

project = Path(__file__).resolve().parent.parent

file_path = project / "data" / "selected_flight.csv"
df = pd.read_csv(file_path)

df = df.sort_values("time").reset_index(drop=True)

df["datetime"] = pd.to_datetime(
    df["time"], unit="s", utc=True
)

columns = ["baroaltitude", "velocity", "vertrate", "lastposupdate"]
df["missing_data"] = df[columns].isna().any(axis=1)

df["position_age"] = df["time"] - df["lastposupdate"]
df["stale_position"] = df["position_age"] > 20

df["time_diff"] = df["time"].diff()
df["altitude_diff"] = df["baroaltitude"].diff()

df["calculated_rate"] = (
    df["altitude_diff"] / df["time_diff"]
)

df["rate_difference"] = (
    df["calculated_rate"] - df["vertrate"]
).abs()

RATE_LIMIT = 20
DIFFERENCE_LIMIT = 15

valid_pair = (
    df["time_diff"].gt(0)
    & df["time_diff"].le(20)
    & df["position_age"].between(0, 20)
    & df["position_age"].shift(1).between(0, 20)
    & df["calculated_rate"].notna()
    & df["vertrate"].notna()
)

df["rapid_altitude_change"] = (
    valid_pair
    & (df["calculated_rate"].abs() > RATE_LIMIT)
)

df["rate_mismatch"] = (
    valid_pair
    & (df["rate_difference"] > DIFFERENCE_LIMIT)
)

flags = [
    "missing_data",
    "stale_position",
    "rapid_altitude_change",
    "rate_mismatch"
]

df["data_quality_issue"] = df[flags].any(axis=1)

print("Aircraft:", df["icao24"].iloc[0])
print("Total records:", len(df))

print("\nData quality results:")
for flag in flags:
    print(flag, ":", int(df[flag].sum()))

print("\nTotal flagged records:")
print(int(df["data_quality_issue"].sum()))

result_columns = [
    "datetime",
    "baroaltitude",
    "position_age",
    "calculated_rate",
    "rate_difference"
] + flags

flagged = df[df["data_quality_issue"]]

print("\nFlagged measurements:")
print(flagged[result_columns].to_string(index=False))

output = project / "data" / "anomaly_results.csv"
df.to_csv(output, index=False)

print("\nResults saved:", output)