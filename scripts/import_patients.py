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
            print(f"CSV file not found at {DATA_PATH}")
            return

        print(f"Loading data from {DATA_PATH}")

        # (Re)create tables if they don't exist
        db.create_all()

        count = 0
        with DATA_PATH.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Expecting CSV columns that match the stroke dataset, e.g.:
                # gender, age, hypertension, heart_disease, ever_married,
                # work_type, Residence_type, avg_glucose_level, bmi,
                # smoking_status, stroke

                gender = row.get("gender")
                age = int(float(row.get("age", 0)))

                hypertension = int(row.get("hypertension", 0))
                heart_disease = int(row.get("heart_disease", 0))

                ever_married = row.get("ever_married")
                work_type = row.get("work_type")
                residence_type = row.get("Residence_type") or row.get("residence_type")

                avg_glucose_level = float(row.get("avg_glucose_level", 0) or 0)

                bmi_raw = row.get("bmi")
                bmi = float(bmi_raw) if bmi_raw not in (None, "", "N/A") else None

                smoking_status = row.get("smoking_status", "Unknown")

                stroke_raw = row.get("stroke")
                if stroke_raw in (None, "", "None"):
                    stroke = None
                else:
                    stroke = int(stroke_raw)

                patient = Patient(
                    gender=gender,
                    age=age,
                    hypertension=hypertension,
                    heart_disease=heart_disease,
                    ever_married=ever_married,
                    work_type=work_type,
                    residence_type=residence_type,
                    avg_glucose_level=avg_glucose_level,
                    bmi=bmi,
                    smoking_status=smoking_status,
                    stroke=stroke,
                )

                db.session.add(patient)
                count += 1

            db.session.commit()
            print(f"Imported {count} patients from {DATA_PATH}")


if __name__ == "__main__":
    import_patients()
