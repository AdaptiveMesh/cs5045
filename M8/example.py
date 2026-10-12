"""
Module 8: Data Cleaning & Wrangling
CS 5045: Computation for the Data Sciences
Virginia Tech: Applied Data Science MS Program

Demonstrates end-to-end data cleaning and wrangling on a messy survey dataset.
Topics: handling missing values, standardizing categories, removing duplicates,
fixing data types, all framed through the five computational operations.

Run from the Code/ directory:
    python3 example.py
"""

import pandas as pd

# ── REPRESENT: Load the raw, messy data ───────────────────────────────────────
print("=" * 60)
print("REPRESENT: Load raw survey data")
print("=" * 60)

df = pd.read_csv("../Datasets/data.csv")
print(f"Shape (rows, columns): {df.shape}")
print(df.head(6))
print()

# Quick inventory of the mess
print("--- Data types ---")
print(df.dtypes)
print()

print("--- Missing values per column ---")
print(df.isnull().sum())
print()

# ── TRANSFORM: Standardize inconsistent text categories ───────────────────────
print("=" * 60)
print("TRANSFORM: Standardize inconsistent categories")
print("=" * 60)

# 'gender' has mixed case: Female / male / FEMALE / Male
print("Unique values in 'gender' before cleaning:")
print(df["gender"].unique())

df["gender"] = df["gender"].str.strip().str.title()

print("Unique values in 'gender' after .str.title():")
print(df["gender"].unique())
print()

# 'employed' has Yes / yes / YES / No
print("Unique values in 'employed' before cleaning:")
print(df["employed"].unique())

df["employed"] = df["employed"].str.strip().str.title()
print("Unique values in 'employed' after .str.title():")
print(df["employed"].unique())
print()

# 'health_rating' has mixed case: Good / good
df["health_rating"] = df["health_rating"].str.strip().str.title()
print("Unique values in 'health_rating' after standardizing:")
print(df["health_rating"].unique())
print()

# 'smoker' has multiple representations: No / no / NO / Yes / YES / Y / N
print("Unique values in 'smoker' before cleaning:")
print(df["smoker"].unique())

# Map all variants to a standard Yes/No
smoker_map = {
    "Yes": "Yes", "yes": "Yes", "YES": "Yes", "Y": "Yes",
    "No": "No",  "no": "No",  "NO": "No",  "N": "No",
}
df["smoker"] = df["smoker"].map(smoker_map)
print("Unique values in 'smoker' after mapping:")
print(df["smoker"].unique())
print()

# ── FILTER: Remove duplicate rows ─────────────────────────────────────────────
print("=" * 60)
print("FILTER: Remove duplicate rows")
print("=" * 60)

print(f"Rows before dropping duplicates: {len(df)}")
df = df.drop_duplicates()
print(f"Rows after dropping duplicates:  {len(df)}")
print()

# ── TRANSFORM: Handle missing values ──────────────────────────────────────────
print("=" * 60)
print("TRANSFORM: Handle missing values")
print("=" * 60)

# 'age' has one NA -- fill with the median (robust to outliers)
print(f"Missing 'age' values: {df['age'].isnull().sum()}")
median_age = df["age"].median()
df["age"] = df["age"].fillna(median_age)
print(f"Filled missing 'age' with median: {median_age}")
print()

# 'income_usd' has one NA -- fill with the median income
print(f"Missing 'income_usd' values: {df['income_usd'].isnull().sum()}")
median_income = df["income_usd"].median()
df["income_usd"] = df["income_usd"].fillna(median_income)
print(f"Filled missing 'income_usd' with median: {median_income}")
print()

# ── TRANSFORM: Fix data types ──────────────────────────────────────────────────
print("=" * 60)
print("TRANSFORM: Fix data types")
print("=" * 60)

# After fillna, 'age' may still be float because pandas uses float for columns
# that had NAs. Convert to int now that NAs are gone.
df["age"] = df["age"].astype(int)
print("Converted 'age' from float to int.")

print("\nData types after cleaning:")
print(df.dtypes)
print()

# ── TRANSFORM: Create a derived column (age group) ────────────────────────────
print("=" * 60)
print("TRANSFORM: Create a new derived column: age_group")
print("=" * 60)

def classify_age(age):
    """Classify a respondent into a broad age group."""
    if age < 35:
        return "Young Adult"
    elif age < 50:
        return "Middle Aged"
    else:
        return "Older Adult"

df["age_group"] = df["age"].apply(classify_age)
print(df[["response_id", "age", "age_group"]].to_string(index=False))
print()

# ── FILTER: Subset to employed respondents only ───────────────────────────────
print("=" * 60)
print("FILTER: Keep only employed respondents")
print("=" * 60)

employed_df = df[df["employed"] == "Yes"]
print(f"Total respondents: {len(df)}")
print(f"Employed respondents: {len(employed_df)}")
print()

# ── AGGREGATE: Summarize health ratings by age group ──────────────────────────
print("=" * 60)
print("AGGREGATE: Mean satisfaction score by age group")
print("=" * 60)

summary = df.groupby("age_group")["satisfaction_score"].mean().round(2)
print(summary)
print()

# ── COMMUNICATE: Final clean dataset overview ─────────────────────────────────
print("=" * 60)
print("COMMUNICATE: Final cleaned dataset")
print("=" * 60)

print(f"Rows: {len(df)},  Columns: {len(df.columns)}")
print(df.to_string(index=False))
print()
print("Cleaning complete. Dataset is ready for analysis.")
