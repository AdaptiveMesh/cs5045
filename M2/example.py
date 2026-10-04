"""
Module 2: Data Representation & Number Systems
CS 5045 — Computation for the Data Sciences
Virginia Tech — Applied Data Science MS Program

This script demonstrates how computers REPRESENT information — the first and most
fundamental of the five computational operations. Every data science pipeline begins
with representation: choosing the right container for your data.

Run this script from the Code/ directory:
    python3 example.py
"""

import pandas as pd

# =============================================================================
# SECTION 1: Representing individual values
# =============================================================================
# Before we think about datasets, we think about single pieces of information.
# Each value has a TYPE — the computer's way of knowing what kind of thing it is
# and what operations make sense on it.

# REPRESENT: whole numbers (int) — used for counts, identifiers, ranks
num_cities = 16
year_recorded = 2023

# REPRESENT: decimal numbers (float) — used for measured quantities
avg_global_temp_c = 15.0          # degrees Celsius
equator_latitude = 0.0

# REPRESENT: text (str) — used for labels, names, categories
dataset_name = "World City Climate Data"
unit_temperature = "Celsius"

# REPRESENT: true/false facts (bool) — used for binary conditions
data_loaded = True
has_missing_values = False

print("=== SECTION 1: Individual Values ===")
print(f"Dataset:    {dataset_name}")
print(f"Cities:     {num_cities}  (type: {type(num_cities).__name__})")
print(f"Global avg: {avg_global_temp_c}°C  (type: {type(avg_global_temp_c).__name__})")
print(f"Tropical?   {has_missing_values}  (type: {type(has_missing_values).__name__})")
print()

# =============================================================================
# SECTION 2: Representing a dataset — loading data from a file
# =============================================================================
# REPRESENT: a DataFrame is how pandas stores a table in memory.
# pd.read_csv() reads the file from disk and creates the in-memory representation.

df = pd.read_csv("data.csv")   # REPRESENT: load the dataset

print("=== SECTION 2: Loading the Dataset ===")
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print()
print(df.head())
print()

# =============================================================================
# SECTION 3: Inspecting types — what does Python think each column is?
# =============================================================================
# REPRESENT: the dtype of each column tells us how pandas stores that column.
# Getting types right matters — arithmetic on strings produces errors, not numbers.

print("=== SECTION 3: Column Data Types ===")
print(df.dtypes)
print()

# Demonstrate the four Python primitive types found in this dataset:
sample = df.iloc[0]   # first row as a reference
print("--- Types in the first row (Nairobi) ---")
print(f"  city          → {type(sample['city']).__name__:>8}  value: {sample['city']}")
print(f"  avg_temp_c    → {type(sample['avg_temp_c']).__name__:>8}  value: {sample['avg_temp_c']}")
print(f"  avg_rainfall_mm → {type(sample['avg_rainfall_mm']).__name__:>8}  value: {sample['avg_rainfall_mm']}")
print(f"  is_tropical   → {type(sample['is_tropical']).__name__:>8}  value: {sample['is_tropical']}")
print()

# =============================================================================
# SECTION 4: Representing temperature in two systems — same fact, different encoding
# =============================================================================
# TRANSFORM: the dataset already has both Celsius and Fahrenheit.
# Here we verify the relationship and show that the same physical fact
# can be represented in more than one way.

print("=== SECTION 4: Two Representations of Temperature ===")
print("The dataset stores temperature as both Celsius and Fahrenheit.")
print("Both columns REPRESENT the same real-world quantity, just encoded differently.\n")

# Verify the conversion formula: F = C × 9/5 + 32
df["temp_f_check"] = df["avg_temp_c"] * 9 / 5 + 32   # TRANSFORM: recompute F from C
df["rounding_error"] = (df["temp_f_check"] - df["avg_temp_f"]).abs()

print(df[["city", "avg_temp_c", "avg_temp_f", "temp_f_check", "rounding_error"]].head(6))
print()

# =============================================================================
# SECTION 5: Type matters — what goes wrong when types are wrong
# =============================================================================
# REPRESENT: choosing the wrong type causes silent errors or outright failures.

print("=== SECTION 5: Why Types Matter ===")

# Safe: arithmetic on float columns
avg_temp = df["avg_temp_c"].mean()          # AGGREGATE: mean of numeric column
print(f"Mean temperature across all cities: {avg_temp:.1f}°C")

# Safe: boolean column can be summed (True=1, False=0)
tropical_count = df["is_tropical"].sum()    # AGGREGATE: count True values
print(f"Number of tropical cities in dataset: {int(tropical_count)} of {len(df)}")
print()

# Demonstrate: reading a numeric column back as string would prevent arithmetic
test_series = df["avg_temp_c"].astype(str)  # simulate wrong type
print("If avg_temp_c were stored as strings:")
try:
    _ = test_series + 1   # this will fail with TypeError
except TypeError as e:
    print(f"  TypeError: {e}")
print()

# =============================================================================
# SECTION 6: Summary — the Represent operation in a pipeline
# =============================================================================
# COMMUNICATE: show a clean summary of the dataset

print("=== SECTION 6: Summary Statistics ===")
print("Numeric columns, descriptive statistics:")
print(df[["avg_temp_c", "avg_temp_f", "avg_rainfall_mm"]].describe().round(2))
print()
print("Categorical breakdown:")
print(f"  Countries represented: {df['country'].nunique()}")
print(f"  Tropical cities:       {df['is_tropical'].sum()}")
print(f"  Non-tropical cities:   {(~df['is_tropical']).sum()}")
print()
print("Represent is always the first step: you cannot filter, transform,")
print("aggregate, or communicate data that is not yet in memory.")
