from pathlib import Path
import subprocess
import gzip
import pandas as pd

project = Path(__file__).resolve().parent.parent
archive = project / "data" / "states_2019-01-07-12.tar"

csv_name = "states_2019-01-07-12.csv.gz"

aircraft_id = "400d8d"

process = subprocess.Popen(
    ["tar", "-xOf", str(archive), csv_name],
    stdout=subprocess.PIPE
)

matches = []

try:
    with gzip.GzipFile(fileobj=process.stdout) as csv_stream:
        for chunk in pd.read_csv(
            csv_stream,
            chunksize=50000,
            dtype={"icao24": "string", "callsign": "string", "squawk": "string"}
        ):
            selected = chunk[chunk["icao24"] == aircraft_id]
            if not selected.empty:
                matches.append(selected.copy())
finally:
    if process.stdout:
        process.stdout.close()
    return_code = process.wait()

if return_code != 0:
    raise RuntimeError("Could not read the flight archive.")

if not matches:
    print("No records found for:", aircraft_id)
    raise SystemExit(1)

flight = pd.concat(matches, ignore_index=True)

flight = flight.sort_values("time")

flight = flight.dropna(subset=["baroaltitude"])

output = project / "data" / "selected_flight.csv"
flight.to_csv(output, index=False)

print("Aircraft:", aircraft_id)
print("Number of records:", len(flight))
print("Unique timestamps:", flight["time"].nunique())

print("First timestamp:")
print(pd.to_datetime(flight["time"].min(), unit="s", utc=True))

print("Last timestamp:")
print(pd.to_datetime(flight["time"].max(), unit="s", utc=True))

print("Saved to:", output)