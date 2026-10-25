"""
Module 10: Multidimensional Data & GroupBy
CS 5045: Computation for the Data Sciences

Demonstrates aggregation across multiple dimensions using pandas GroupBy.
Dataset: retail sales data (region, product_category, quarter, units_sold, revenue).

Run from the Code/ directory:
    python3 example.py
"""

import pandas as pd
import matplotlib.pyplot as plt

# REPRESENT: load the dataset into a DataFrame
# Every analysis starts by bringing data into memory in a form we can work with.
df = pd.read_csv("data.csv")

print("=== REPRESENT: raw data ===")
print(df)
print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Columns: {list(df.columns)}")

# AGGREGATE: collapse rows into summaries
# GroupBy splits the dataset into groups, applies a function to each group,
# and combines the results -- a Split, Apply, Combine pattern.

print("\n=== AGGREGATE: total revenue by region ===")
# Single-key groupby: one grouping dimension
by_region = df.groupby("region")["revenue"].sum()
print(by_region)

print("\n=== AGGREGATE: total units sold by product category ===")
by_category = df.groupby("product_category")["units_sold"].sum()
print(by_category)

# AGGREGATE across multiple dimensions
# Multidimensional groupby: pass a list of column names.
# This answers "what is the total revenue for each region AND category?"
print("\n=== AGGREGATE: total revenue by region AND product category ===")
by_region_category = df.groupby(["region", "product_category"])["revenue"].sum()
print(by_region_category)

# AGGREGATE: multiple statistics at once
# .agg() lets you compute several summary statistics in a single call.
print("\n=== AGGREGATE: summary stats by region (mean revenue, total units) ===")
region_summary = df.groupby("region").agg(
    mean_revenue=("revenue", "mean"),
    total_units=("units_sold", "sum"),
    num_records=("revenue", "count")
)
print(region_summary)

# COMMUNICATE: grouped bar chart -- visualize group summaries
# .plot(kind='bar') turns a pandas Series or DataFrame into a bar chart.
print("\n=== COMMUNICATE: bar chart of total revenue by region ===")
by_region.plot(
    kind="bar",
    title="Total Revenue by Region",
    ylabel="Revenue ($)"
)
plt.xlabel("Region")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("revenue_by_region.png", dpi=100)
plt.close()
print("Saved: revenue_by_region.png")

# Grouped bar chart: two categories side by side per region
pivot_cat = (
    df.groupby(["region", "product_category"])["revenue"].sum()
    .unstack()
)
pivot_cat.plot(kind="bar")
plt.title("Revenue by Region and Product Category")
plt.xlabel("Region")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=45)
plt.legend(title="Category")
plt.tight_layout()
plt.savefig("revenue_by_region_category.png", dpi=100)
plt.close()
print("Saved: revenue_by_region_category.png")

# TRANSFORM: pivot a grouped result into a readable table
# .unstack() moves one level of the index to become column headers,
# turning a long result into a wide, cross-tabular layout.
print("\n=== TRANSFORM: revenue pivot table (region x quarter) ===")
pivot = df.groupby(["region", "quarter"])["revenue"].sum().unstack(fill_value=0)
print(pivot)

# FILTER then AGGREGATE: narrow first, then summarize
# These two operations compose naturally.
print("\n=== FILTER + AGGREGATE: Electronics only, total revenue by region ===")
electronics = df[df["product_category"] == "Electronics"]   # Filter
elec_revenue = electronics.groupby("region")["revenue"].sum()  # Aggregate
print(elec_revenue)

# AGGREGATE: group by quarter
print("\n=== AGGREGATE: revenue by quarter across all regions and categories ===")
by_quarter = df.groupby("quarter")["revenue"].sum()
print(by_quarter)

# COMMUNICATE: format the multidimensional result clearly
# A well-labeled summary is more useful than raw numbers.
print("\n=== COMMUNICATE: top region by revenue ===")
top_region = by_region.idxmax()
top_revenue = by_region.max()
print(f"Highest-revenue region: {top_region}  (${top_revenue:,.0f} total)")

print("\n=== COMMUNICATE: formatted revenue summary table ===")
region_summary_sorted = region_summary.sort_values("mean_revenue", ascending=False)
print(region_summary_sorted.to_string())
