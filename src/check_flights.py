from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "flights.csv"

df = pd.read_csv(file_path)

print("Total rows:", len(df))
print("Unique aircraft:", df["icao24"].nunique())

print("Unique timestamps:", df["time"].nunique())

print("\nAircraft with the most records:")
print(df["icao24"].value_counts().head(10))

print("\nFirst timestamp:")
print(pd.to_datetime(df["time"].min(), unit="s", utc=True))

print("\nLast timestamp:")
print(pd.to_datetime(df["time"].max(), unit="s", utc=True))
