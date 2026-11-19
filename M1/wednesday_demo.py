# Module 1 — Wednesday Session Demo
# CS 5045: Computation for the Data Sciences
#
# This script is for live use during the Wednesday session.
# Run it top-to-bottom with students, pausing at each labeled section.
# Uses health_survey.csv from the same folder as this script.
#
# Run from the Wednesday_Session folder:
#   python3 wednesday_demo.py
# Or load in an interactive environment and run cell by cell.

import pandas as pd

DATA_PATH = "health_survey.csv"

# ── REPRESENT ─────────────────────────────────────────────────────────────────
#
# Every computation starts here: get the data into memory.
# Pause here and ask: what does df look like? How big is it?

df = pd.read_csv(DATA_PATH)

print("=== REPRESENT: What did we just load? ===")
print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
print(df)

print("\n--- Column types ---")
print(df.dtypes)

print("\n--- Summary statistics ---")
print(df.describe())

# ── FILTER ────────────────────────────────────────────────────────────────────
#
# A filter asks a yes/no question about every row and keeps only the "yes" rows.
# The question here: is this patient's blood pressure above 130?
#
# Pause here: how many rows do we expect? Check the original table.
# Ask students: what question is Python asking about each row?

print("\n=== FILTER: Patients with systolic BP above 130 ===")

# Show the boolean series first — what Python evaluates for each row
print("\n--- What does the condition alone produce? ---")
print(df["systolic_bp"] > 130)

# Now use that True/False series to keep only the matching rows
high_bp = df[df["systolic_bp"] > 130]

print(f"\nStarted with {len(df)} patients. Filter kept {len(high_bp)}.")
print(high_bp[["patient_id", "age", "smoker", "systolic_bp"]])

# Second filter: non-smokers only
print("\n--- Before running: how many non-smokers do you expect? ---")
non_smokers = df[df["smoker"] == "no"]
print(f"Non-smokers: {len(non_smokers)}")
print(non_smokers[["patient_id", "age", "systolic_bp"]])

# ── TRANSFORM ─────────────────────────────────────────────────────────────────
#
# A transform doesn't remove rows — it adds or changes information.
# Here we compute BMI for every patient and store it as a new column.
#
# Pause here: how many rows in df after this? Same as before.
# Ask students: what's the difference between this and the filter above?

print("\n=== TRANSFORM: Add a BMI column ===")

df["bmi"] = df["weight_kg"] / (df["height_cm"] / 100) ** 2

print(df[["patient_id", "weight_kg", "height_cm", "bmi"]].round(1))

# One more transform: flag patients as high-risk (BP > 130 OR smoker)
df["high_risk"] = (df["systolic_bp"] > 130) | (df["smoker"] == "yes")

print("\nWith high-risk flag:")
print(df[["patient_id", "systolic_bp", "smoker", "high_risk"]])

# ── AGGREGATE ─────────────────────────────────────────────────────────────────
#
# An aggregate collapses many rows into one (or a few) summary values.
# We go from 12 rows to 2 numbers — one per group.
#
# Pause here: before running, ask students what they expect the numbers to be.
# Then run and compare.

print("\n=== AGGREGATE: Average BP by smoking status ===")

# Overall average first
overall_avg = df["systolic_bp"].mean()
print(f"Average systolic BP (all patients): {overall_avg:.1f} mmHg")

# Then by group
avg_by_smoker = df.groupby("smoker")["systolic_bp"].mean().round(1)
print(avg_by_smoker)

# Count of high-risk patients
n_high_risk = df["high_risk"].sum()
print(f"\nHigh-risk patients: {n_high_risk} of {len(df)}")

# ── COMMUNICATE ───────────────────────────────────────────────────────────────
#
# Everything above was for the computer. This is for a human.
# A print statement is the simplest form of Communicate.
# A plot, a table, a report — all Communicate.
#
# Pause here: this is the only output a non-programmer would ever see.
# The five operations all led to this moment.

print("\n=== COMMUNICATE: Summary findings ===")

n_high_bp   = len(high_bp)
bp_smokers  = avg_by_smoker.get("yes", float("nan"))
bp_nonsmokers = avg_by_smoker.get("no",  float("nan"))

print(f"""
Patient Health Survey — Summary
--------------------------------
Total patients:          {len(df)}
High BP (> 130):         {n_high_bp}
High risk (BP or smoker): {n_high_risk}

Average systolic BP:
  Smokers:     {bp_smokers} mmHg
  Non-smokers: {bp_nonsmokers} mmHg
""")

# ── WRAP UP ───────────────────────────────────────────────────────────────────
#
# Ask students: which lines of the assignment map to which operations?
# The goal: they leave knowing exactly what each assignment task is asking them to do.
