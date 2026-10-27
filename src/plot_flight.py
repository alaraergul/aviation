from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

project = Path(__file__).resolve().parent.parent

file_path = project / "data" / "selected_flight.csv"
df = pd.read_csv(file_path)

df["datetime"] = pd.to_datetime(
    df["time"], unit="s", utc=True
)

df = df.sort_values("time").copy()

df["time_gap"] = df["time"].diff()

print("Aircraft:", df["icao24"].iloc[0])
print("Number of records:", len(df))

print("\nTime gaps in seconds:")
print(df["time_gap"].describe())

print("\nGaps longer than 20 seconds:")
print((df["time_gap"] > 20).sum())

figures = project / "data" / "figures"
figures.mkdir(parents=True, exist_ok=True)

measurements = [
    ("baroaltitude", "Barometric Altitude", "Altitude (m)", "altitude.png"),
    ("velocity", "Ground Speed", "Speed (m/s)", "velocity.png"),
    ("vertrate", "Vertical Rate", "Vertical Rate (m/s)", "vertical_rate.png"),
]

for column, title, ylabel, filename in measurements:

    valid = df.dropna(subset=[column]).copy()

    if valid.empty:
        print("No valid measurements for:", column)
        continue

    plt.figure(figsize=(10, 5))

    valid["gap"] = valid["time"].diff()
    valid["segment"] = (valid["gap"] > 20).cumsum()

    for _, segment in valid.groupby("segment"):
        plt.plot(
            segment["datetime"],
            segment[column],
            marker=".",
            markersize=3,
            linewidth=1.5
        )

    plt.title(title + " Over Time")
    plt.xlabel("Time (UTC)")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=30)
    plt.tight_layout()

    output = figures / filename
    plt.savefig(output, dpi=150)
    plt.close()

    print("Saved:", output)

print("\nAnalysis complete!")