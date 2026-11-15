"""
Module 13: Web Data & APIs
CS 5045: Computation for the Data Sciences
Virginia Tech, Kurt Stein

Demonstrates the full API pipeline using Open-Meteo, a free weather API
that requires no account or API key.

Five operations:
    Represent : fetch JSON from a URL; save to file; load into DataFrame
    Filter    : keep only days with measurable precipitation
    Transform : convert Celsius to Fahrenheit; label warm vs. cool days
    Aggregate : mean temperature and precipitation by temperature label
    Communicate: line plot of max and min temperature over 7 days

Run from this folder:
    python example.py

Open-Meteo URL used:
    https://api.open-meteo.com/v1/forecast
    Parameters: latitude=37.2296, longitude=-80.4139 (Blacksburg VA)
                daily=temperature_2m_max,temperature_2m_min,precipitation_sum
                timezone=America/New_York
"""

import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# Section 1: REPRESENT: Fetch data from Open-Meteo
# --------------------------------------------------------------------------
print("=" * 60)
print("REPRESENT: Fetching 7-day weather forecast from Open-Meteo")
print("=" * 60)

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude":  37.2296,
    "longitude": -80.4139,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "America/New_York",
}

response = requests.get(URL, params=PARAMS)

if response.status_code != 200:
    print(f"Error: status {response.status_code}")
    raise SystemExit(1)

data = response.json()
print(f"Status: {response.status_code}  (200 = success)")
print(f"Top-level keys: {list(data.keys())}")
print(f"Daily keys: {list(data['daily'].keys())}")
print()

# Save the response so later sections can reload without a network call
with open("weather_response.json", "w") as f:
    json.dump(data, f, indent=2)
print("Saved: weather_response.json")
print()

# --------------------------------------------------------------------------
# Section 2: REPRESENT: Load from saved file; build DataFrame
# --------------------------------------------------------------------------
print("=" * 60)
print("REPRESENT: Loading from saved file -> DataFrame")
print("=" * 60)

with open("weather_response.json") as f:
    data = json.load(f)

df = pd.DataFrame(data["daily"])

# Rename columns for readability
df = df.rename(columns={
    "temperature_2m_max": "temp_max_c",
    "temperature_2m_min": "temp_min_c",
    "precipitation_sum":  "precip_mm",
})

print(df.to_string(index=False))
print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")
print()

loaded_rows, loaded_cols = df.shape

# --------------------------------------------------------------------------
# Section 3: FILTER: Days with measurable precipitation
# --------------------------------------------------------------------------
print("=" * 60)
print("FILTER: Days with measurable precipitation (precip_mm > 0)")
print("=" * 60)

rainy_days = df[df["precip_mm"] > 0]
print(rainy_days[["time", "temp_max_c", "precip_mm"]].to_string(index=False))
print(f"\n{len(rainy_days)} of {len(df)} days have measurable precipitation.")
print()

# --------------------------------------------------------------------------
# Section 4: TRANSFORM: Fahrenheit conversion; warm vs. cool label
# --------------------------------------------------------------------------
print("=" * 60)
print("TRANSFORM: Adding temp_max_f and day_label columns")
print("=" * 60)

df["temp_max_f"] = (df["temp_max_c"] * 9 / 5) + 32
df["temp_min_f"] = (df["temp_min_c"] * 9 / 5) + 32


def day_label(temp_c):
    """
    TRANSFORM: classify a maximum temperature as Warm or Cool.

    Parameters:
        temp_c (float): daily maximum temperature in Celsius

    Returns:
        str: 'Warm' if temp_c >= 25, else 'Cool'
    """
    return "Warm" if temp_c >= 25 else "Cool"


df["day_label"] = df["temp_max_c"].apply(day_label)

print(df[["time", "temp_max_c", "temp_max_f", "day_label"]].to_string(index=False))
print()

# --------------------------------------------------------------------------
# Section 5: AGGREGATE: Mean temperature and precipitation by label
# --------------------------------------------------------------------------
print("=" * 60)
print("AGGREGATE: Mean values by day label")
print("=" * 60)

summary = df.groupby("day_label").agg(
    days=("time", "count"),
    mean_max_c=("temp_max_c", "mean"),
    mean_precip=("precip_mm", "mean"),
).round(1)
print(summary)
print()

# --------------------------------------------------------------------------
# Section 6: COMMUNICATE: Line plot of max and min temperature
# --------------------------------------------------------------------------
print("=" * 60)
print("COMMUNICATE: Generating temperature line plot")
print("=" * 60)

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df["time"], df["temp_max_c"], marker="o", color="#861F41",
        linewidth=2, label="Daily Max (C)")
ax.plot(df["time"], df["temp_min_c"], marker="o", color="#4393c3",
        linewidth=2, label="Daily Min (C)")

ax.fill_between(df["time"], df["temp_min_c"], df["temp_max_c"],
                alpha=0.15, color="#861F41", label="Range")

ax.set_title("7-Day Temperature Forecast: Blacksburg, VA", fontsize=13)
ax.set_xlabel("Date", fontsize=11)
ax.set_ylabel("Temperature (C)", fontsize=11)
ax.tick_params(axis="x", rotation=30)
ax.legend(fontsize=10)
ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.6)

plt.tight_layout()
plt.savefig("forecast_plot.png", dpi=150)
print("Saved: forecast_plot.png")
plt.close()

# --------------------------------------------------------------------------
# Pipeline summary
# --------------------------------------------------------------------------
print("\n" + "=" * 60)
print("PIPELINE SUMMARY")
print("=" * 60)
print(f"  Represent  : Fetched 7-day forecast; saved as weather_response.json")
print(f"  Represent  : Loaded JSON into DataFrame ({loaded_rows} rows x {loaded_cols} cols)")
print(f"  Filter     : {len(rainy_days)} rainy days (precip_mm > 0)")
print(f"  Transform  : Converted C to F; labeled {df['day_label'].nunique()} day categories")
print(f"  Aggregate  : Summarized by day label")
print(f"  Communicate: Saved line plot to forecast_plot.png")
