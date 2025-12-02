#======================================================================
#Machine Learning utilities for the Stroke Risk Prediction application.

#This module provides:
#load_model(): loads the trained Logistic Regression model from disk
# predict_stroke(): applies the ML model to patient feature data

#The trained model is saved in: models/stroke_model.joblib
#and is loaded once when predictions are needed.

#This file intentionally contains only lightweight ML logic
#because the full training pipeline is handled separately
#in scripts/train_model.py.
#=======================================================================

from pathlib import Path
from typing import Optional, Tuple

import joblib
import pandas as pd

from .models import Patient

_model = None
_model_version: Optional[str] = None

# -------------------------
# Load the trained ML model
# -------------------------
# Returns a loaded Logistic Regression model from joblib.
# If loading fails, it returns None (handled gracefully in routes).

def _load_model():
    global _model, _model_version
    if _model is not None:
        return _model

    model_path = Path("models/stroke_model.joblib")
    if not model_path.exists():
        raise RuntimeError(
            f"Model file not found at {model_path}. "
            "Run scripts/train_model.py first."
        )

    bundle = joblib.load(model_path)
    if isinstance(bundle, dict) and "pipeline" in bundle:
        _model = bundle["pipeline"]
        _model_version = bundle.get("version")
    else:
        _model = bundle
        _model_version = None
    return _model


def get_model_version() -> Optional[str]:
    _load_model()
    return _model_version

# -------------------------
# Generate Stroke Prediction
# -------------------------
# Takes a dictionary of patient features and returns:
#probability of stroke (0 to 1)
#predicted class (0 or 1)
# Features are processed into the correct order expected by the model.
# Missing values (e.g., BMI) are replaced with 0 or defaults

def predict_for_patient(patient: Patient) -> Tuple[float, int]:

    model = _load_model()

    features = {
        "gender": patient.gender,
        "age": patient.age,
        "hypertension": int(bool(patient.hypertension)),
        "heart_disease": int(bool(patient.heart_disease)),
        "ever_married": patient.ever_married,
        "work_type": patient.work_type,
        "residence_type": patient.residence_type,
        "avg_glucose_level": patient.avg_glucose_level,
        "bmi": patient.bmi,
        "smoking_status": patient.smoking_status,
    }

    X = pd.DataFrame([features])
    proba = model.predict_proba(X)[0][1]
    label = int(model.predict(X)[0])
    return float(proba), label
