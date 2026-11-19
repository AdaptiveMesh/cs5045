"""
Module 5: Functions & Modularity
CS 5045: Computation for the Data Sciences

Demonstrates how functions package reusable computational operations.
Dataset: road race results (runner_id, name, finish_time_min, age, gender, category)

Run from the Code/ folder:
    python3 example.py
"""

import pandas as pd
import os

# ── Load Data ──────────────────────────────────────────────────────────────────
# REPRESENT: read the dataset from CSV into a DataFrame
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")
df = pd.read_csv(DATA_PATH)

print("=== Race Results Dataset ===")
print(df.to_string(index=False))
print()

# ── Why Functions? ─────────────────────────────────────────────────────────────
# Without functions, every repeated calculation gets copy-pasted.
# With functions, each operation has a name, a clear purpose, and a single home.

# ── Defining Functions ─────────────────────────────────────────────────────────

def pace_per_km(finish_time_min, distance_km=10.0):
    """
    TRANSFORM: compute pace in minutes per kilometer.

    Parameters:
        finish_time_min (float) -- runner's finish time in minutes
        distance_km (float)     -- race distance in km (default: 10.0)

    Returns:
        float -- pace in minutes per km, rounded to 2 decimal places
    """
    return round(finish_time_min / distance_km, 2)


def age_group(age):
    """
    TRANSFORM: classify a runner into an age group string.

    Parameters:
        age (int) -- runner's age in years

    Returns:
        str -- age group label: 'Under 30', '30-39', '40-49', or '50+'
    """
    if age < 30:
        return "Under 30"
    elif age < 40:
        return "30-39"
    elif age < 50:
        return "40-49"
    else:
        return "50+"


def is_podium(finish_time_min, cutoff=41.0):
    """
    FILTER: return True if finish time qualifies for a podium spot.

    Parameters:
        finish_time_min (float) -- runner's finish time in minutes
        cutoff (float)          -- podium cutoff time in minutes (default: 41.0)

    Returns:
        bool -- True if finish_time_min <= cutoff
    """
    return finish_time_min <= cutoff


def summarize_category(dataframe, category_name):
    """
    AGGREGATE: compute mean, min, and max finish time for one category.

    Parameters:
        dataframe (DataFrame) -- the full race results DataFrame
        category_name (str)   -- the category to filter for ("Open" or "Masters")

    Returns:
        dict -- {"mean": float, "min": float, "max": float}
    """
    group = dataframe[dataframe["category"] == category_name]
    return {
        "mean": float(round(group["finish_time_min"].mean(), 2)),
        "min":  float(group["finish_time_min"].min()),
        "max":  float(group["finish_time_min"].max()),
    }


def print_leaderboard(data, top_n=5):
    """
    COMMUNICATE: print the top-N runners sorted by finish time.

    Parameters:
        data (DataFrame) -- race results DataFrame
        top_n (int)      -- number of runners to display (default: 5)
    """
    leaders = data.nsmallest(top_n, "finish_time_min")[
        ["name", "finish_time_min", "age", "gender", "category"]
    ]
    print(f"=== Top {top_n} Finishers ===")
    print(leaders.to_string(index=False))
    print()


# ── Apply Functions to the Dataset ────────────────────────────────────────────

# TRANSFORM: add a pace column using the pace_per_km function
df["pace_min_per_km"] = df["finish_time_min"].apply(pace_per_km)

# TRANSFORM: add an age_group column using the age_group function
df["age_group"] = df["age"].apply(age_group)

# FILTER: identify podium finishers using the is_podium function
df["is_podium"] = df["finish_time_min"].apply(is_podium)
podium_runners = df[df["is_podium"]]

print("=== Podium Finishers (finish time <= 41 min) ===")
print(podium_runners[["name", "finish_time_min", "pace_min_per_km", "age_group"]].to_string(index=False))
print()

# AGGREGATE: summarize results by category
masters_summary = summarize_category(df, "Masters")
open_summary    = summarize_category(df, "Open")
print("=== Summary by Category ===")
print("Masters:", masters_summary)
print("Open:   ", open_summary)
print()

# COMMUNICATE: display the leaderboard
print_leaderboard(df, top_n=5)

# ── Default Arguments and Reuse ────────────────────────────────────────────────
# The same pace_per_km function works for a different distance; no rewriting needed.
print("=== Pace Recalculated for a 5K Race ===")
df["pace_5k"] = df["finish_time_min"].apply(lambda t: pace_per_km(t, distance_km=5.0))
print(df[["name", "finish_time_min", "pace_min_per_km", "pace_5k"]].head(6).to_string(index=False))
print()

# ── Scope Demo ─────────────────────────────────────────────────────────────────
# Variables defined inside a function stay inside that function.
def demo_scope():
    """Illustrates that local variables do not leak out of a function."""
    local_var = "I only exist inside demo_scope"
    return local_var

result = demo_scope()
print("=== Scope Demo ===")
print("Return value:", result)
# print(local_var)  # <- would raise NameError; local_var is not accessible here

print()
print("=== Final Dataset with Derived Columns ===")
print(df[["name", "finish_time_min", "pace_min_per_km", "age_group", "is_podium"]].to_string(index=False))
