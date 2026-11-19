"""
Module 14: Looking Ahead: Machine Learning
CS 5045: Computation for the Data Sciences
Virginia Tech, Kurt Stein

A preview, not a mastery demo: one linear regression, on the same air-quality
dataset from Module 9, showing what changes (and what doesn't) when a rule is
learned from data instead of written by hand. Model selection, classification,
and deeper evaluation are ADS 5525 / CS 5046 territory, not here.

Five operations, reframed for this one week:
    Represent: same data.csv as Module 9, no changes
    (rule): Modules 1-13, you wrote the rule. This week: model.fit() learns it.
    Aggregate: R-squared and MAE collapse many prediction errors into one number
    Communicate: predicted-vs-actual scatter plot

Run from this folder:
    python example.py
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# --------------------------------------------------------------------------
# Section 1: REPRESENT: same dataset as Module 9, no changes
# --------------------------------------------------------------------------
print("=" * 60)
print("REPRESENT: Loading the Module 9 air-quality dataset")
print("=" * 60)

# data.csv sits next to this script on GitHub; locally it is in ../Datasets
data_path = Path("data.csv") if Path("data.csv").exists() else Path("../Datasets/data.csv")
df = pd.read_csv(data_path)
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(df.head())
print()

# --------------------------------------------------------------------------
# Section 2: TRAIN / TEST SPLIT: the new idea this week
# --------------------------------------------------------------------------
print("=" * 60)
print("SPLIT: Holding out 20% of the data the model never trains on")
print("=" * 60)

FEATURES = ["ozone", "temp_c", "humidity"]
TARGET = "pm25"

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training rows: {len(X_train)}")
print(f"Test rows:     {len(X_test)}  (the model never sees these during fitting)")
print()

# --------------------------------------------------------------------------
# Section 3: FIT: the model learns its own rule from the training rows
# --------------------------------------------------------------------------
print("=" * 60)
print("FIT: model.fit() learns a rule; nobody wrote it by hand")
print("=" * 60)

model = LinearRegression()
model.fit(X_train, y_train)

print("Learned coefficients (one per input):")
for feature, coef in zip(FEATURES, model.coef_):
    print(f"  {feature:10s}: {coef:8.3f}")
print(f"  intercept : {model.intercept_:8.3f}")
print()
print("Nobody wrote these numbers. train_test_split gave the model 240 examples")
print("of (ozone, temp_c, humidity) -> pm25, and fit() worked backward to the")
print("line that comes closest to all of them at once.")
print()

# --------------------------------------------------------------------------
# Section 4: EVALUATE: AGGREGATE many prediction errors into one score
# --------------------------------------------------------------------------
print("=" * 60)
print("AGGREGATE: One score, summarizing every prediction on the test set")
print("=" * 60)

predictions = model.predict(X_test)
r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

print(f"R-squared: {r2:.3f}   (1.0 = perfect; 0.0 = no better than guessing the mean)")
print(f"MAE:       {mae:.2f} micrograms/m^3   (average size of a miss, in the original units)")
print()
print("0.330 is a moderate fit, not an impressive one, and that's the honest, useful")
print("result. Ozone, temperature, and humidity only partly explain air quality. The")
print("rest comes from things this model was never given: wildfire smoke, traffic,")
print("local industry, wind direction. A model can only learn from what it's shown.")
print()

# --------------------------------------------------------------------------
# Section 5: WHERE IT'S WRONG: the model's biggest miss on held-out data
# --------------------------------------------------------------------------
print("=" * 60)
print("WHERE IT'S WRONG: The single largest miss on the test set")
print("=" * 60)

results = X_test.copy()
results["actual_pm25"] = y_test.values
results["predicted_pm25"] = predictions.round(1)
results["miss"] = (results["predicted_pm25"] - results["actual_pm25"]).round(1)
results["city"] = df.loc[y_test.index, "city"].values
results["date"] = df.loc[y_test.index, "date"].values

worst = results.reindex(results["miss"].abs().sort_values(ascending=False).index).head(3)
print(worst[["city", "date", "actual_pm25", "predicted_pm25", "miss"]].to_string(index=False))
print()
print("Biggest miss: Houston, 2023-12-10: actual pm25 was 20.0, the model said 12.8,")
print("a 7.2 miss. The model only ever saw ozone, temperature, and humidity for that day.")
print("Anything else going on in Houston that week (a traffic spike, a refinery event,")
print("an inversion layer trapping pollution near the ground) was invisible to it.")
print("A model's mistakes point directly at what it was never given.")
print()

# --------------------------------------------------------------------------
# Section 6: COMMUNICATE: predicted vs. actual
# --------------------------------------------------------------------------
print("=" * 60)
print("COMMUNICATE: Predicted vs. actual pm25 on the test set")
print("=" * 60)

fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(results["actual_pm25"], results["predicted_pm25"],
           color="#861F41", alpha=0.75, edgecolor="white", s=60)

lims = [
    min(results["actual_pm25"].min(), results["predicted_pm25"].min()) - 1,
    max(results["actual_pm25"].max(), results["predicted_pm25"].max()) + 1,
]
ax.plot(lims, lims, linestyle="--", color="#666666", linewidth=1.5, label="Perfect prediction")

ax.set_xlim(lims)
ax.set_ylim(lims)
ax.set_xlabel("Actual pm25 (micrograms/m^3)", fontsize=11)
ax.set_ylabel("Predicted pm25 (micrograms/m^3)", fontsize=11)
ax.set_title("Predicted vs. Actual: Test Set Only", fontsize=13)
ax.legend(fontsize=10)
ax.grid(linestyle="--", linewidth=0.5, alpha=0.6)

plt.tight_layout()
plt.savefig("predicted_vs_actual.png", dpi=150)
print("Saved: predicted_vs_actual.png")
plt.close()

# --------------------------------------------------------------------------
# Pipeline summary
# --------------------------------------------------------------------------
print("\n" + "=" * 60)
print("PIPELINE SUMMARY")
print("=" * 60)
print(f"  Represent : Loaded the same 300-row air-quality dataset as Module 9")
print(f"  Split     : 240 training rows, 60 held-out test rows")
print(f"  Learned   : model.fit() found a rule; nobody wrote it by hand")
print(f"  Aggregate : R-squared = {r2:.3f}, MAE = {mae:.2f} on test data the model never trained on")
print(f"  Communicate: Saved predicted_vs_actual.png")
print(f"  Next      : ADS 5525 / CS 5046 covers model selection, classification, and deeper evaluation")
