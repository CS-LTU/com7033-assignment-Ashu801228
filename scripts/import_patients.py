import os
import sys
import csv
from pathlib import Path

# Make sure the project root (stroke-risk-app) is on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db
from app.models import Patient


DATA_PATH = Path("data/patients.csv")


def import_patients():
    app = create_app()
    with app.app_context():
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"CSV not found: {DATA_PATH}")

        count = 0
        with DATA_PATH.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # If dataset has ID but no name, synthesise a pseudonym
                full_name = row.get("full_name") or f"Patient {row.get('id', count+1)}"

                patient = Patient(
                    full_name=full_name,
                    gender=row.get("gender"),
                    age=float(row["age"]) if row.get("age") else None,
                    hypertension=row.get("hypertension") in ("1", "True", "true"),
                    heart_disease=row.get("heart_disease") in ("1", "True", "true"),
                    ever_married=row.get("ever_married"),
                    work_type=row.get("work_type"),
                    residence_type=row.get("Residence_type") or row.get("residence_type"),
                    avg_glucose_level=float(row["avg_glucose_level"])
                    if row.get("avg_glucose_level")
                    else None,
                    bmi=float(row["bmi"]) if row.get("bmi") else None,
                    smoking_status=row.get("smoking_status"),
                    stroke=row.get("stroke") in ("1", "True", "true"),
                )
                db.session.add(patient)
                count += 1

            db.session.commit()
        print(f"Imported {count} patients from {DATA_PATH}")


if __name__ == "__main__":
    import_patients()
