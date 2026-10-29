from pathlib import Path
import pandas as pd

project = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    project / "data" / "anomaly_results.csv"
)

total = len(df)
flagged = int(df["data_quality_issue"].sum())

missing = int(df["missing_data"].sum())
stale = int(df["stale_position"].sum())
rapid = int(df["rapid_altitude_change"].sum())
mismatch = int(df["rate_mismatch"].sum())

percentage = flagged / total * 100 if total else 0

report = f"""# Flight Data Quality Report

## Aircraft Information

Aircraft ICAO24: {df["icao24"].iloc[0]}
Total records: {total}
Dataset: OpenSky State Vectors
Date: 2019-01-07

## Data Quality Results

| Check | Flagged records |
|---|---:|
| Missing measurements | {missing} |
| Stale position information | {stale} |
| Rapid altitude changes | {rapid} |
| Vertical rate mismatch | {mismatch} |

Total flagged records: {flagged}
Flagged percentage: {percentage:.2f}%

## Method

The system checks four data quality conditions:

1. Missing measurements in selected fields.
2. Position information older than 20 seconds.
3. Altitude change rates greater than 20 m/s.
4. Difference between calculated and reported
   vertical rates greater than 15 m/s.

The thresholds are experimental and are not
official aviation safety limits.

## Findings

The system identified {flagged} records with
at least one data quality flag.

The different checks can flag the same record,
so their individual counts should not be added
together to calculate the total.

## Limitations

This analysis uses one aircraft's records from
a limited time interval.

The results identify possible measurement
issues, not confirmed aircraft failures or
unsafe flight events.

More aircraft and time periods are needed
before evaluating how well these rules
generalize.
"""

output = project / "data" / "flight_quality_report.md"
output.write_text(report, encoding="utf-8")

print(report)
print("\nReport saved:", output)