from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

project_folder = Path(__file__).resolve().parent.parent

file_path = project_folder / "data" / "flights.csv"

if not file_path.exists():
    print("Flight data file not found!")
    print("Expected location:", file_path)
    raise SystemExit(1)


df = pd.read_csv(file_path)

print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isna().sum())

if "baroaltitude" in df.columns:
    altitude = pd.to_numeric(
        df["baroaltitude"], errors="coerce"
    ).dropna()

    if not altitude.empty:
        plt.figure(figsize=(9, 4))
        plt.plot(altitude.to_numpy())
        plt.title("Recorded Aircraft Altitude")
        plt.xlabel("Record index")
        plt.ylabel("Barometric altitude (m)")
        plt.tight_layout()

        output = project_folder / "data" / "altitude.png"
        plt.savefig(output)
        plt.close()

        print("\nChart saved:", output)