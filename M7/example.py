"""
Module 7: Data Science Ethics
CS 5045: Computation for the Data Sciences
Virginia Tech

Demonstrates bias detection and fairness analysis on a loan application dataset.
Shows how the five computational operations (Represent, Filter, Transform,
Aggregate, Communicate) each carry ethical weight when applied to real data
about people.

Self-contained: the dataset is embedded below, so this file runs anywhere,
no companion CSV needed. It mirrors Datasets/data.csv; if that file is ever
regenerated, re-embed these rows to match.

Run from anywhere:
    python3 example.py
"""

import pandas as pd

# == REPRESENT =================================================================
# Load the dataset into memory. Every Represent decision is an ethical one:
# Which columns were collected? Who decided what to measure? What is missing?
print("=" * 60)
print("REPRESENT: Loading loan application data")
print("=" * 60)

loan_applications = [
    {"applicant_id": "A001", "age": 34, "income": 52000, "zip_code": 24060, "race_category": "White", "credit_score": 720, "loan_amount": 15000, "approved": 1, "default_rate": 0.04},
    {"applicant_id": "A002", "age": 27, "income": 38000, "zip_code": 24061, "race_category": "Black", "credit_score": 680, "loan_amount": 12000, "approved": 0, "default_rate": 0.07},
    {"applicant_id": "A003", "age": 45, "income": 75000, "zip_code": 22903, "race_category": "White", "credit_score": 760, "loan_amount": 25000, "approved": 1, "default_rate": 0.02},
    {"applicant_id": "A004", "age": 31, "income": 41000, "zip_code": 24061, "race_category": "Hispanic", "credit_score": 650, "loan_amount": 10000, "approved": 0, "default_rate": 0.09},
    {"applicant_id": "A005", "age": 52, "income": 91000, "zip_code": 22901, "race_category": "White", "credit_score": 800, "loan_amount": 40000, "approved": 1, "default_rate": 0.01},
    {"applicant_id": "A006", "age": 29, "income": 35000, "zip_code": 24060, "race_category": "Black", "credit_score": 670, "loan_amount": 8000, "approved": 0, "default_rate": 0.11},
    {"applicant_id": "A007", "age": 41, "income": 63000, "zip_code": 22902, "race_category": "Asian", "credit_score": 740, "loan_amount": 20000, "approved": 1, "default_rate": 0.03},
    {"applicant_id": "A008", "age": 38, "income": 57000, "zip_code": 24061, "race_category": "Hispanic", "credit_score": 700, "loan_amount": 18000, "approved": 1, "default_rate": 0.05},
    {"applicant_id": "A009", "age": 24, "income": 29000, "zip_code": 24060, "race_category": "Black", "credit_score": 620, "loan_amount": 7000, "approved": 0, "default_rate": 0.14},
    {"applicant_id": "A010", "age": 55, "income": 110000, "zip_code": 22903, "race_category": "White", "credit_score": 820, "loan_amount": 50000, "approved": 1, "default_rate": 0.01},
    {"applicant_id": "A011", "age": 33, "income": 48000, "zip_code": 22901, "race_category": "Hispanic", "credit_score": 690, "loan_amount": 14000, "approved": 0, "default_rate": 0.08},
    {"applicant_id": "A012", "age": 47, "income": 82000, "zip_code": 22902, "race_category": "White", "credit_score": 775, "loan_amount": 30000, "approved": 1, "default_rate": 0.02},
    {"applicant_id": "A013", "age": 26, "income": 32000, "zip_code": 24061, "race_category": "Black", "credit_score": 640, "loan_amount": 9000, "approved": 0, "default_rate": 0.12},
    {"applicant_id": "A014", "age": 36, "income": 61000, "zip_code": 22903, "race_category": "Asian", "credit_score": 730, "loan_amount": 22000, "approved": 1, "default_rate": 0.03},
    {"applicant_id": "A015", "age": 43, "income": 70000, "zip_code": 24060, "race_category": "White", "credit_score": 755, "loan_amount": 28000, "approved": 1, "default_rate": 0.03},
    {"applicant_id": "A016", "age": 30, "income": 39000, "zip_code": 24061, "race_category": "Black", "credit_score": 660, "loan_amount": 11000, "approved": 0, "default_rate": 0.10},
    {"applicant_id": "A017", "age": 50, "income": 95000, "zip_code": 22901, "race_category": "White", "credit_score": 810, "loan_amount": 45000, "approved": 1, "default_rate": 0.01},
    {"applicant_id": "A018", "age": 28, "income": 36000, "zip_code": 24060, "race_category": "Hispanic", "credit_score": 645, "loan_amount": 8500, "approved": 0, "default_rate": 0.13},
]

df = pd.DataFrame(loan_applications)
print(df.head())
print(f"\nDataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
print("\nColumn names:", list(df.columns))
print("\nData types:\n", df.dtypes)

# Notice: zip_code looks numeric but is a categorical identifier.
# Treating it as a number in a model would be an ethical and technical mistake.
df["zip_code"] = df["zip_code"].astype(str)

# == FILTER ====================================================================
# Filtering creates subgroups. Filtering decisions determine who is
# included in an analysis and who is left out.
print("\n" + "=" * 60)
print("FILTER: Examining approved vs. denied applicants")
print("=" * 60)

approved = df[df["approved"] == 1]   # Filter: keep only approved applicants
denied   = df[df["approved"] == 0]   # Filter: keep only denied applicants

print(f"\nApproved applicants: {len(approved)}")
print(f"Denied applicants:   {len(denied)}")

# Filter to look at applicants with similar credit scores but different outcomes.
borderline = df[(df["credit_score"] >= 640) & (df["credit_score"] <= 700)]
print(f"\nBorderline credit score (640-700) applicants: {len(borderline)}")
print(borderline[["applicant_id", "age", "income", "credit_score",
                   "race_category", "approved"]])

# == TRANSFORM =================================================================
# Transform creates new information from existing columns.
# Every derived variable embeds assumptions; inspect those assumptions.
print("\n" + "=" * 60)
print("TRANSFORM: Computing derived features")
print("=" * 60)

# Debt-to-income ratio: a common proxy variable in lending models.
# Proxy variables can encode protected characteristics indirectly.
df["debt_to_income"] = (df["loan_amount"] / df["income"]).round(3)
print("\nDebt-to-income ratio added:")
print(df[["applicant_id", "loan_amount", "income", "debt_to_income",
          "race_category", "approved"]].head(10))

# Flag applications where income is below the median. A threshold like this
# can have disparate impact across demographic groups.
income_median = df["income"].median()
df["below_median_income"] = (df["income"] < income_median).astype(int)
print(f"\nMedian income: ${income_median:,.0f}")
print("Below-median flag by race:")
print(df.groupby("race_category")["below_median_income"].mean().round(2))

# == AGGREGATE =================================================================
# Aggregation summarizes many values into one. When we aggregate across
# demographic groups, we can see, or obscure, disparities.
print("\n" + "=" * 60)
print("AGGREGATE: Approval rates by demographic group")
print("=" * 60)

# Approval rate by race: the key fairness metric.
approval_by_race = df.groupby("race_category")["approved"].mean().round(3)
print("\nApproval rate by racial category:")
print(approval_by_race.to_string())

# Average credit score by race: is the denial rate explained by credit score,
# or is there a residual effect after controlling for credit?
credit_by_race = df.groupby("race_category")["credit_score"].mean().round(1)
print("\nAverage credit score by racial category:")
print(credit_by_race.to_string())

# Approval rate and average credit score side by side.
summary = pd.DataFrame({
    "approval_rate":    approval_by_race,
    "avg_credit_score": credit_by_race
})
print("\nSummary table (approval rate vs. average credit score):")
print(summary.to_string())

# Default rate among approved applicants: did the model predict risk accurately
# across groups, or does it over-predict risk for some groups?
approved_df = df[df["approved"] == 1]
default_by_race = approved_df.groupby("race_category")["default_rate"].mean().round(3)
print("\nAverage default rate among approved applicants, by race:")
print(default_by_race.to_string())

# == COMMUNICATE ===============================================================
# Communicate presents results to a human. HOW we communicate findings
# shapes what decisions get made. Burying a disparity in a footnote is
# a choice with ethical consequences.
print("\n" + "=" * 60)
print("COMMUNICATE: Surfacing the disparity clearly")
print("=" * 60)

print("""
FINDINGS SUMMARY
----------------
This dataset shows a pattern common in real-world lending data:

1. Approval rates differ dramatically by racial category (Asian and White 100%,
   Hispanic 25%, Black 0%), and the gap is fully explained by one clean rule:
   every applicant with credit_score >= 700 is approved, every applicant below
   it is denied, no exceptions. The rule never looks at race.

2. But credit_score is not race-neutral in this data. Average credit score by
   race is Asian 735, White 777, Hispanic 671, Black 654. A race-blind cutoff
   applied to a race-correlated input still produces a racially disparate
   outcome: this is disparate impact through a proxy variable.

3. The borderline credit-score band (640-700), where the cutoff actually
   decides anything, is made up entirely of Black and Hispanic applicants.
   No White or Asian applicant in this dataset has a score below 720. The
   cutoff has no power to divide White or Asian applicants at all; it only
   ever operates on Black and Hispanic ones.

4. Among approved applicants, default rates still differ by race (Asian 0.03,
   Hispanic 0.05, White 0.02), but Black applicants do not appear in that
   table at all, because zero Black applicants were approved. The exclusion
   happens so early that there is no data left to check whether the model
   would have treated them fairly afterward.

ETHICAL QUESTIONS THIS RAISES
------------------------------
- A rule that never mentions race still sorted applicants almost entirely by
  race. Does removing a protected column from a model prevent disparate impact?
- Was zip_code also used as a feature? (It correlates strongly with race too.)
- Who decided where to set the credit-score cutoff? What would a different
  cutoff change about who gets approved, and who gets a chance to be audited
  at all?
- Who had access to these decisions? Who was harmed by them?

DATA SCIENTISTS ARE NOT NEUTRAL
---------------------------------
Every decision in this analysis: which columns to collect, which threshold
to use, which groups to compare, is a choice. Choices have consequences.
""")
