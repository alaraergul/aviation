from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

project = Path(__file__).resolve().parent.parent

file_path = project / "data" / "anomaly_results.csv"
df = pd.read_csv(file_path)

df["datetime"] = pd.to_datetime(
    df["time"], unit="s", utc=True
)

df = df.sort_values("time")

rapid = df[df["rapid_altitude_change"]]
mismatch = df[df["rate_mismatch"]]
stale = df[df["stale_position"]]

plt.figure(figsize=(12, 6))

plt.plot(
    df["datetime"],
    df["baroaltitude"],
    color="steelblue",
    linewidth=1.5,
    label="Recorded altitude"
)

plt.scatter(
    rapid["datetime"],
    rapid["baroaltitude"],
    color="red",
    marker="x",
    s=90,
    linewidths=2,
    label="Rapid altitude change",
    zorder=4
)

plt.scatter(
    mismatch["datetime"],
    mismatch["baroaltitude"],
    facecolors="none",
    edgecolors="darkorange",
    s=170,
    linewidths=2,
    label="Vertical rate mismatch",
    zorder=5
)

plt.scatter(
    stale["datetime"],
    stale["baroaltitude"],
    color="purple",
    marker="s",
    s=22,
    label="Stale position",
    zorder=3
)

plt.title("Aircraft Altitude and Data Quality Flags")
plt.xlabel("Time (UTC)")
plt.ylabel("Barometric Altitude (m)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.xticks(rotation=30)
plt.tight_layout()

output = project / "data" / "figures"
output.mkdir(parents=True, exist_ok=True)

chart_path = output / "anomaly_detection.png"
plt.savefig(chart_path, dpi=160)
plt.close()

print("Chart saved:", chart_path)
print("Rapid altitude flags:", len(rapid))
print("Rate mismatch flags:", len(mismatch))
print("Stale position flags:", len(stale))