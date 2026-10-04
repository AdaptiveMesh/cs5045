"""
Introduction to Computation — Complete Worked Example
CS 5045 — Computation for the Data Sciences

This script demonstrates the five computational operations using a patient health survey.
Run it top to bottom. You do not need to understand every line yet — just observe
what each section does and what it produces.

The five operations:
  Represent  — store information so a computer can work with it
  Filter     — keep only the rows that meet a condition
  Transform  — change or create values
  Aggregate  — collapse many values into one summary
  Communicate — present results to a human
"""

import pandas as pd
import matplotlib.pyplot as plt

# ── THE BIG PICTURE: a complete data science pipeline in ~10 lines ─────────────
# Run this first. We will spend the rest of the semester understanding every part.

df = pd.read_csv("health_survey.csv")          # Represent
smokers = df[df["smoker"] == "yes"]                        # Filter
df["bmi"] = df["weight_kg"] / (df["height_cm"] / 100)**2  # Transform
avg_bp = df.groupby("smoker")["systolic_bp"].mean()        # Aggregate
print(avg_bp)                                              # Communicate

# ──────────────────────────────────────────────────────────────────────────────
# Now let's look at each operation more carefully.
# ──────────────────────────────────────────────────────────────────────────────

# ----- REPRESENT: storing information ----------------------------------------
# Variables are named containers. Python figures out the type automatically.

course_name  = "Computation for the Data Sciences"   # str  — text
num_students = 28                                     # int  — whole number
avg_age      = 44.5                                   # float — decimal
is_online    = True                                   # bool — True or False

print("\n--- Variables ---")
print(f"Course: {course_name}")
print(f"Students: {num_students}")
print(f"Average patient age: {avg_age}")

# The same idea applies to an entire dataset:
print("\n--- Dataset: first five rows ---")
print(df.head())
print(f"\nShape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"\nColumn types:\n{df.dtypes}")

# ----- FILTER: keeping only what we need -------------------------------------
print("\n--- Filter: patients over 50 ---")
older_patients = df[df["age"] > 50]
print(older_patients[["patient_id", "age", "smoker", "systolic_bp"]])

print("\n--- Filter: smokers only ---")
print(smokers[["patient_id", "age", "systolic_bp"]])

# ----- TRANSFORM: creating new values ----------------------------------------
# BMI was already computed above. Let's also create a risk label.
print("\n--- Transform: BMI and risk category ---")

def bp_category(bp):
    if bp < 120:
        return "normal"
    elif bp < 130:
        return "elevated"
    else:
        return "high"

df["bp_category"] = df["systolic_bp"].apply(bp_category)
print(df[["patient_id", "systolic_bp", "bp_category", "bmi"]].round(1))

# ----- AGGREGATE: summarizing many values into one ---------------------------
print("\n--- Aggregate: summary statistics ---")
print(df["systolic_bp"].describe().round(1))

print("\n--- Aggregate: average BP by smoker status ---")
print(avg_bp.round(1))

print("\n--- Aggregate: BP category counts ---")
print(df["bp_category"].value_counts())

# ----- COMMUNICATE: showing results to a human -------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Histogram: blood pressure distribution
axes[0].hist(df["systolic_bp"], bins=6, color="steelblue", edgecolor="white")
axes[0].set_title("Blood Pressure Distribution")
axes[0].set_xlabel("Systolic BP (mmHg)")
axes[0].set_ylabel("Number of Patients")

# Bar chart: average BP by smoking status
avg_bp.plot(kind="bar", ax=axes[1], color=["steelblue", "tomato"], edgecolor="white")
axes[1].set_title("Average Systolic BP by Smoking Status")
axes[1].set_xlabel("Smoker")
axes[1].set_ylabel("Average Systolic BP (mmHg)")
axes[1].tick_params(axis="x", rotation=0)

plt.tight_layout()
plt.savefig("computation_intro_plots.png", dpi=150)
plt.show()
print("\nPlot saved to computation_intro_plots.png")
print("\nDone. Five operations: Represent, Filter, Transform, Aggregate, Communicate.")
