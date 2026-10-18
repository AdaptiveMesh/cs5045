"""
Module 9: Exploratory Data Analysis and Visualization
CS 5045 - Computation for the Data Sciences

Demonstrates a full EDA pipeline using air quality monitoring data.
Operations covered: Represent, Aggregate, Communicate (with Filter and Transform support).

Dataset: 300 air quality readings across 6 US cities.
Columns: city, date, pm25 (fine particulate matter ug/m3), ozone (ppm),
         temp_c (temperature in Celsius), humidity (%).

CRISP-DM context: this script covers the Data Understanding phase.
Run EDA before any modeling or reporting.

Run from this directory:
    python3 example.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# -- REPRESENT ----------------------------------------------------------------
# Load the dataset from CSV into a DataFrame; bringing raw data into memory
# so every subsequent operation can work with it.
# CRISP-DM: Data Understanding begins here.

df = pd.read_csv("data.csv")

print("=== REPRESENT: Dataset loaded ===")
print(df.head())
print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isna().sum()}")


# -- AGGREGATE (summary statistics) ------------------------------------------
# Collapse the full dataset into one-number summaries for each numeric column.
# This is EDA step 1: get your bearings on scale, spread, and center.

print("\n=== AGGREGATE: Summary statistics (all cities combined) ===")
print(df[["pm25", "ozone", "temp_c", "humidity"]].describe().round(2))


# -- AGGREGATE (group-by city) ------------------------------------------------
# Collapse measurements within each city into per-city averages.
# GroupBy is the most common Aggregate pattern in data science.

print("\n=== AGGREGATE: Mean values by city ===")
city_means = df.groupby("city")[["pm25", "ozone", "temp_c", "humidity"]].mean().round(2)
print(city_means)


# -- FILTER + AGGREGATE -------------------------------------------------------
# Keep only high-pollution readings (pm25 > 15), then summarize by city.
# Combining Filter and Aggregate is one of the most useful EDA patterns.

print("\n=== FILTER + AGGREGATE: High-pollution readings (pm25 > 15) ===")
high_pm25 = df[df["pm25"] > 15]
print(f"  {len(high_pm25)} rows meet the condition (out of {len(df)} total)")
print(high_pm25[["city", "date", "pm25", "ozone"]].to_string(index=False))


# -- TRANSFORM ----------------------------------------------------------------
# Create a new column that categorizes each row.
# Transform produces a new value for every row without changing the originals.

def aq_label(pm25_value):
    """
    TRANSFORM: return an EPA-style air quality label based on PM2.5 concentration.

    Parameters:
        pm25_value (float) -- PM2.5 concentration in ug/m3

    Returns:
        str -- one of 'Good', 'Moderate', or 'Unhealthy'
    """
    if pm25_value < 12:
        return "Good"
    elif pm25_value < 20:
        return "Moderate"
    else:
        return "Unhealthy"

df["aq_cat"] = df["pm25"].apply(aq_label)

print("\n=== TRANSFORM: Air quality category added ===")
print(df[["city", "date", "pm25", "aq_cat"]].to_string(index=False))


# -- AGGREGATE: count by category --------------------------------------------
print("\n=== AGGREGATE: Count of readings per air quality category ===")
category_counts = df["aq_cat"].value_counts()
print(category_counts)


# -- COMMUNICATE: Bar chart and scatter plot ----------------------------------
# Present the city-level aggregate as a bar chart for a human audience.
# Communicate operations turn numbers into insights a reader can act on.

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left panel: mean PM2.5 by city
city_means["pm25"].sort_values(ascending=False).plot(
    kind="bar", ax=axes[0], color="#861F41", edgecolor="white"
)
axes[0].set_title("Mean PM2.5 by City", fontsize=13, fontweight="bold")
axes[0].set_xlabel("City", fontsize=11)
axes[0].set_ylabel("PM2.5 (ug/m3)", fontsize=11)
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=30, ha="right")
axes[0].axhline(12, color="steelblue", linestyle="--", linewidth=1.2,
                label="Good threshold (12 ug/m3)")
axes[0].legend(fontsize=9)

# Right panel: PM2.5 vs. temperature (scatter to look for a pattern)
for city, grp in df.groupby("city"):
    axes[1].scatter(grp["temp_c"], grp["pm25"], label=city, s=60, alpha=0.8)

axes[1].set_title("PM2.5 vs. Temperature", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Temperature (C)", fontsize=11)
axes[1].set_ylabel("PM2.5 (ug/m3)", fontsize=11)
axes[1].legend(fontsize=9)

plt.suptitle("Module 9: Air Quality EDA", fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("air_quality_eda.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n=== COMMUNICATE: Plot saved as air_quality_eda.png ===")


# -- COMMUNICATE: Summary table for a non-technical reader -------------------
print("\n=== COMMUNICATE: City summary for a non-technical audience ===")
summary = df.groupby("city").agg(
    readings=("pm25", "count"),
    avg_pm25=("pm25", "mean"),
    max_pm25=("pm25", "max"),
    avg_ozone=("ozone", "mean"),
).round(2)
print(summary.to_string())

print("\nDone. All five operations demonstrated end-to-end.")
print("CRISP-DM: this script covers the Data Understanding phase.")
