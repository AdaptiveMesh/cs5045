"""
Module 6: Object-Oriented Programming
CS 5045: Computation for the Data Sciences
Virginia Tech, Applied Data Science MS Program

Demonstrates how object-oriented programming organizes the five computational
operations (Represent, Filter, Transform, Aggregate, Communicate) by bundling
data and the actions that act on that data into a single unit called a class.

Dataset: data.csv  (patient records)

Run from the Code/ folder:
    python3 example.py
"""

import csv
import math


# =============================================================================
# REPRESENT: define the blueprint for what a Patient looks like
# =============================================================================

class Patient:
    """
    A Patient bundles two things together:
      - attributes: the data that describes a single patient
      - methods: the operations we commonly perform on that data

    This is the Represent operation at the object level: instead of storing
    data in loose variables or scattered CSV rows, we create a structured
    container that knows what a "patient" is.
    """

    def __init__(self, patient_id, first_name, last_name, age, sex,
                 diagnosis, systolic_bp, diastolic_bp, cholesterol,
                 bmi, smoker, num_visits):
        """Initialize a Patient with all attributes from one CSV row."""
        self.patient_id   = patient_id
        self.first_name   = first_name
        self.last_name    = last_name
        self.age          = int(age)
        self.sex          = sex
        self.diagnosis    = diagnosis
        self.systolic_bp  = int(systolic_bp)
        self.diastolic_bp = int(diastolic_bp)
        self.cholesterol  = int(cholesterol)
        self.bmi          = float(bmi)
        self.smoker       = smoker.lower() == "yes"   # store as True/False
        self.num_visits   = int(num_visits)

    # -------------------------------------------------------------------------
    # TRANSFORM: methods that compute new values from a patient's attributes
    # -------------------------------------------------------------------------

    def pulse_pressure(self):
        """
        Transform: compute pulse pressure (systolic minus diastolic).
        Pulse pressure > 60 mmHg is a clinical risk indicator.
        """
        return self.systolic_bp - self.diastolic_bp

    def is_high_risk(self):
        """
        Transform: return True if the patient meets any high-risk criterion.
        Criteria: systolic BP >= 140, BMI >= 30, or smoker with diagnosis != Healthy.
        """
        hypertensive = self.systolic_bp >= 140
        obese        = self.bmi >= 30
        risky_smoker = self.smoker and self.diagnosis != "Healthy"
        return hypertensive or obese or risky_smoker

    def risk_label(self):
        """Transform: return a human-readable risk label."""
        return "High Risk" if self.is_high_risk() else "Standard Risk"

    def full_name(self):
        """Transform: combine first and last name into one string."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Communicate: a readable summary when a Patient is printed."""
        return (f"Patient({self.patient_id}, {self.full_name()}, "
                f"age={self.age}, {self.diagnosis}, {self.risk_label()})")


# =============================================================================
# REPRESENT: a Clinic holds a collection of Patient objects
# =============================================================================

class Clinic:
    """
    A Clinic manages a list of Patient objects and provides operations
    that act on the entire collection: filter, aggregate, and communicate.

    This separates two levels of responsibility:
      - Patient knows about one person
      - Clinic knows about all people
    """

    def __init__(self, name="General Clinic"):
        self.name     = name
        self.patients = []   # starts empty; we add patients one at a time

    def add_patient(self, patient):
        """Represent: add a Patient object to the collection."""
        self.patients.append(patient)

    def size(self):
        """Aggregate: return the total number of patients."""
        return len(self.patients)

    # -------------------------------------------------------------------------
    # FILTER: methods that return subsets of the patient list
    # -------------------------------------------------------------------------

    def by_diagnosis(self, diagnosis):
        """Filter: return patients whose diagnosis matches the argument."""
        return [p for p in self.patients if p.diagnosis == diagnosis]

    def high_risk(self):
        """Filter: return patients flagged as high risk."""
        return [p for p in self.patients if p.is_high_risk()]

    def older_than(self, age_threshold):
        """Filter: return patients older than a given age."""
        return [p for p in self.patients if p.age > age_threshold]

    # -------------------------------------------------------------------------
    # AGGREGATE: methods that summarize across the collection
    # -------------------------------------------------------------------------

    def mean_systolic_bp(self, subset=None):
        """
        Aggregate: compute average systolic blood pressure.
        If subset is provided, aggregate that list; otherwise use all patients.
        """
        group = subset if subset is not None else self.patients
        if not group:
            return None
        return sum(p.systolic_bp for p in group) / len(group)

    def mean_bmi(self, subset=None):
        """Aggregate: compute average BMI across the given subset or all patients."""
        group = subset if subset is not None else self.patients
        if not group:
            return None
        return sum(p.bmi for p in group) / len(group)

    def avg_cholesterol(self, subset=None):
        """Aggregate: compute average cholesterol across the given subset or all patients."""
        group = subset if subset is not None else self.patients
        if not group:
            return None
        return sum(p.cholesterol for p in group) / len(group)

    def count_by_diagnosis(self):
        """
        Aggregate: count patients in each diagnosis category.
        Returns a dict of {diagnosis: count}.
        """
        counts = {}
        for p in self.patients:
            counts[p.diagnosis] = counts.get(p.diagnosis, 0) + 1
        return counts

    def risk_summary(self):
        """
        Aggregate: count how many patients are high risk vs. standard risk.
        Returns a dict of {label: count}.
        """
        summary = {"High Risk": 0, "Standard Risk": 0}
        for p in self.patients:
            summary[p.risk_label()] += 1
        return summary

    # -------------------------------------------------------------------------
    # COMMUNICATE: methods that display results
    # -------------------------------------------------------------------------

    def print_roster(self, subset=None):
        """Communicate: print a summary row for each patient."""
        group = subset if subset is not None else self.patients
        print(f"\n{'ID':<6} {'Name':<20} {'Age':>4} {'Diagnosis':<15} {'Risk':<14} {'Sys BP':>6}")
        print("-" * 70)
        for p in group:
            print(f"{p.patient_id:<6} {p.full_name():<20} {p.age:>4} "
                  f"{p.diagnosis:<15} {p.risk_label():<14} {p.systolic_bp:>6}")

    def print_summary(self):
        """Communicate: print aggregate statistics for the whole clinic."""
        print(f"\n=== {self.name}: Summary Report ===")
        print(f"Total patients : {self.size()}")
        print(f"Mean systolic BP : {self.mean_systolic_bp():.1f} mmHg")
        print(f"Mean BMI         : {self.mean_bmi():.1f}")
        print(f"Mean cholesterol : {self.avg_cholesterol():.1f}")
        print()
        print("Patients by diagnosis:")
        for diag, count in sorted(self.count_by_diagnosis().items()):
            print(f"  {diag:<15} {count}")
        print()
        print("Risk distribution:")
        for label, count in self.risk_summary().items():
            print(f"  {label:<15} {count}")


# =============================================================================
# REPRESENT: load the CSV file and create Patient objects
# =============================================================================

def load_patients(filepath):
    """
    Represent: read each row of the CSV and construct a Patient object.
    Returns a list of Patient objects; raw data has become structured objects.
    """
    patients = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = Patient(
                patient_id   = row["patient_id"],
                first_name   = row["first_name"],
                last_name    = row["last_name"],
                age          = row["age"],
                sex          = row["sex"],
                diagnosis    = row["diagnosis"],
                systolic_bp  = row["systolic_bp"],
                diastolic_bp = row["diastolic_bp"],
                cholesterol  = row["cholesterol"],
                bmi          = row["bmi"],
                smoker       = row["smoker"],
                num_visits   = row["num_visits"],
            )
            patients.append(p)
    return patients


# =============================================================================
# MAIN: run the full pipeline
# =============================================================================

def main():
    # ── Represent: load data into Patient objects ─────────────────────────────
    patients = load_patients("data.csv")

    clinic = Clinic(name="VT Teaching Clinic")
    for p in patients:
        clinic.add_patient(p)

    print(f"Loaded {clinic.size()} patients into {clinic.name}.")

    # ── Communicate: show the full roster ────────────────────────────────────
    clinic.print_roster()

    # ── Filter: isolate high-risk patients ───────────────────────────────────
    high_risk = clinic.high_risk()
    print(f"\n--- High-Risk Patients ({len(high_risk)} of {clinic.size()}) ---")
    clinic.print_roster(subset=high_risk)

    # ── Filter + Aggregate: compare BP by diagnosis ───────────────────────────
    print("\n--- Mean Systolic BP by Diagnosis ---")
    for diag in ["Healthy", "Hypertension", "Diabetes"]:
        group = clinic.by_diagnosis(diag)
        mean  = clinic.mean_systolic_bp(subset=group)
        print(f"  {diag:<15} n={len(group)}  mean BP = {mean:.1f} mmHg")

    # ── Transform: show pulse pressure for each patient ───────────────────────
    print("\n--- Pulse Pressure (Systolic - Diastolic) ---")
    print(f"{'Name':<22} {'Pulse Pressure':>14}  {'Flag'}")
    print("-" * 50)
    for p in patients:
        pp   = p.pulse_pressure()
        flag = "  *** elevated" if pp > 60 else ""
        print(f"{p.full_name():<22} {pp:>14} mmHg{flag}")

    # ── Communicate: summary statistics ──────────────────────────────────────
    clinic.print_summary()


if __name__ == "__main__":
    main()
