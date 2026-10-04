"""
Module 3: Conditionals & Control Flow
CS 5045: Computation for the Data Sciences
Virginia Tech, Applied Data Science MS Program

Demonstrates Filter and Transform using conditionals (if/elif/else) and
loops (for, while) applied to a student performance dataset.

Dataset: data.csv
  - student_id, name, attendance_pct, assignment_avg, midterm_score,
    final_score, major, study_hours_per_week, passed_midterm
"""

import csv
import os

# ── REPRESENT: Load the dataset ────────────────────────────────────────────────
# Read the CSV into a list of dictionaries so each row is a named record.
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")

students = []
with open(DATA_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Convert numeric columns from strings to numbers.
        row["attendance_pct"]       = float(row["attendance_pct"])
        row["assignment_avg"]       = float(row["assignment_avg"])
        row["midterm_score"]        = float(row["midterm_score"])
        row["final_score"]          = float(row["final_score"])
        row["study_hours_per_week"] = int(row["study_hours_per_week"])
        students.append(row)

print(f"Loaded {len(students)} student records.\n")


# ── TRANSFORM: Assign a letter grade using if/elif/else ───────────────────────
# A conditional tests a condition and routes execution to the matching branch.
# Here we transform each numeric final score into a categorical letter grade.

def assign_grade(score):
    """Return a letter grade for a given numeric score (0–100)."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

# Apply the transform to every student using a for loop.
print("=== TRANSFORM: Assign letter grades ===")
for student in students:
    student["letter_grade"] = assign_grade(student["final_score"])
    print(f"  {student['name']:<20}  final={student['final_score']:5.1f}  grade={student['letter_grade']}")

print()


# ── TRANSFORM: Flag students with low attendance ──────────────────────────────
# A second transform: add an at-risk indicator based on attendance.
# This illustrates a simple binary condition (the most common case).

print("=== TRANSFORM: Identify low-attendance students ===")
ATTENDANCE_THRESHOLD = 75.0   # below this percentage → flagged

for student in students:
    if student["attendance_pct"] < ATTENDANCE_THRESHOLD:
        student["attendance_flag"] = "low"
    else:
        student["attendance_flag"] = "ok"

# Show only the relevant columns so the transform is easy to read.
for s in students:
    flag_label = "** LOW **" if s["attendance_flag"] == "low" else ""
    print(f"  {s['name']:<20}  attendance={s['attendance_pct']:5.1f}%  {flag_label}")

print()


# ── FILTER: Keep only students who passed the midterm ─────────────────────────
# Filter scans every row and keeps only those satisfying the condition.
# Here: passed_midterm == "yes" (a categorical condition).

print("=== FILTER: Students who passed the midterm ===")
passed = []
for student in students:
    if student["passed_midterm"] == "yes":   # condition
        passed.append(student)               # keep this row

print(f"  {len(passed)} of {len(students)} students passed the midterm.\n")
for s in passed:
    print(f"  {s['name']:<20}  midterm={s['midterm_score']:5.1f}")

print()


# ── FILTER: Compound condition: high attendance AND high assignment average ────
# Real-world filters often combine multiple conditions with and / or.

print("=== FILTER: High attendance AND strong assignment average (both >= 85) ===")
high_performers = []
for student in students:
    if student["attendance_pct"] >= 85 and student["assignment_avg"] >= 85:
        high_performers.append(student)

for s in high_performers:
    print(f"  {s['name']:<20}  attendance={s['attendance_pct']:5.1f}%  assignments={s['assignment_avg']:5.1f}")

print(f"\n  {len(high_performers)} students meet both criteria.\n")


# ── TRANSFORM: Compute a composite score with a weighted formula ───────────────
# Transform can also produce a new numeric column from existing ones.
# Here: composite = 30% midterm + 50% final + 20% assignments

print("=== TRANSFORM: Compute composite course score ===")
for student in students:
    student["composite"] = (
        0.30 * student["midterm_score"]
        + 0.50 * student["final_score"]
        + 0.20 * student["assignment_avg"]
    )

for s in students:
    print(f"  {s['name']:<20}  composite={s['composite']:6.2f}")

print()


# ── FILTER + AGGREGATE (manual): Count by letter grade ────────────────────────
# Combine filter and a running count to produce a simple frequency table.
# (In Module 10 you will do this in one line with pandas GroupBy.)

print("=== AGGREGATE: Count students per letter grade ===")
grade_counts = {}
for student in students:
    g = student["letter_grade"]
    if g not in grade_counts:
        grade_counts[g] = 0
    grade_counts[g] += 1

for grade in sorted(grade_counts.keys()):
    print(f"  {grade}: {grade_counts[grade]} student(s)")

print()


# ── COMMUNICATE: Print a summary table ────────────────────────────────────────
# Present the results clearly so a human can read them.

print("=== COMMUNICATE: Final summary table ===")
header = f"{'Name':<20} {'Attend%':>8} {'Midterm':>8} {'Final':>7} {'Grade':>6} {'Flag':>8}"
print(header)
print("-" * len(header))
for s in sorted(students, key=lambda x: x["final_score"], reverse=True):
    print(
        f"  {s['name']:<20} {s['attendance_pct']:>7.1f} "
        f"{s['midterm_score']:>8.1f} {s['final_score']:>7.1f} "
        f"{s['letter_grade']:>6} {s['attendance_flag']:>8}"
    )
