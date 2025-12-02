import argparse
from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


@dataclass
class TrainConfig:
    input_csv: Path
    output_model: Path
    test_size: float = 0.2
    random_state: int = 42
    penalty: str = "l2"
    C: float = 1.0
    max_iter: int = 1000
    solver: str = "lbfgs"
    version: str = "logreg_v1"


def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    df = pd.read_csv(path)

    # Handle different column naming for residence type
    if "Residence_type" in df.columns and "residence_type" not in df.columns:
        df = df.rename(columns={"Residence_type": "residence_type"})

    return df


def build_pipeline(df: pd.DataFrame, cfg: TrainConfig):
    required_cols = [
        "gender",
        "age",
        "hypertension",
        "heart_disease",
        "ever_married",
        "work_type",
        "residence_type",
        "avg_glucose_level",
        "bmi",
        "smoking_status",
        "stroke",
    ]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in CSV: {col}")

    # Drop rows with missing target
    df = df.dropna(subset=["stroke"])

    # Basic type conversions
    df["stroke"] = df["stroke"].astype(int)
    df["hypertension"] = df["hypertension"].astype(int)
    df["heart_disease"] = df["heart_disease"].astype(int)
    df["age"] = df["age"].astype(float)
    df["avg_glucose_level"] = df["avg_glucose_level"].astype(float)
    df["bmi"] = pd.to_numeric(df["bmi"], errors="coerce")
    df.loc[df["bmi"] <= 0, "bmi"] = np.nan

    feature_cols = [
        "gender",
        "age",
        "hypertension",
        "heart_disease",
        "ever_married",
        "work_type",
        "residence_type",
        "avg_glucose_level",
        "bmi",
        "smoking_status",
    ]
    target_col = "stroke"

    X = df[feature_cols].copy()
    y = df[target_col].copy()

    # Handle missing BMI with median imputation
    if "bmi" in X.columns:
        X["bmi"] = X["bmi"].fillna(X["bmi"].median())

    numeric_features = [
        "age",
        "hypertension",
        "heart_disease",
        "avg_glucose_level",
        "bmi",
    ]
    categorical_features = [
        "gender",
        "ever_married",
        "work_type",
        "residence_type",
        "smoking_status",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    clf = LogisticRegression(
        penalty=cfg.penalty,
        C=cfg.C,
        solver=cfg.solver,
        max_iter=cfg.max_iter,
        class_weight="balanced",
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("clf", clf),
        ]
    )

    meta = {
        "feature_cols": feature_cols,
        "target_col": target_col,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
    }

    return pipeline, X, y, meta


def train_and_save(cfg: TrainConfig) -> None:
    print(f"Loading data from {cfg.input_csv}")
    df = load_data(cfg.input_csv)
    pipeline, X, y, meta = build_pipeline(df, cfg)

    n_samples = len(y)
    n_classes = y.nunique()
    print(f"Number of samples: {n_samples}, number of classes: {n_classes}")

    # ---- Small dataset handling ----
    if n_samples < 10 or n_classes < 2:
        print(
            "Dataset too small or only one class present – "
            "training model on all data without a separate test set."
        )
        X_train, X_test, y_train, y_test = X, X, y, y
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=cfg.test_size,
            random_state=cfg.random_state,
            stratify=y,
        )

    print("Training Logistic Regression model...")
    pipeline.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    try:
        y_proba = pipeline.predict_proba(X_test)[:, 1]
    except Exception:
        y_proba = None

    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")

    if y_proba is not None and y_test.nunique() == 2:
        try:
            auc = roc_auc_score(y_test, y_proba)
            print(f"ROC-AUC: {auc:.4f}")
        except ValueError:
            print("ROC-AUC could not be computed (possibly only one class in y_test).")
    else:
        print("Skipping ROC-AUC (no probabilities or only one class).")

    print("Classification report:")
    print(classification_report(y_test, y_pred))

    # Save the model bundle
    cfg.output_model.parent.mkdir(parents=True, exist_ok=True)
    bundle = {
        "pipeline": pipeline,
        "version": cfg.version,
        "meta": meta,
    }
    joblib.dump(bundle, cfg.output_model)
    print(f"Model saved to {cfg.output_model}")


def parse_args() -> TrainConfig:
    parser = argparse.ArgumentParser(description="Train Logistic Regression stroke model.")
    parser.add_argument(
        "--input-csv",
        type=str,
        required=True,
        help="Path to stroke dataset CSV (e.g. data/patients.csv)",
    )
    parser.add_argument(
        "--output-model",
        type=str,
        default="models/stroke_model.joblib",
        help="Where to save the trained model.",
    )
    parser.add_argument(
        "--version",
        type=str,
        default="logreg_v1",
        help="Model version tag to store in the bundle.",
    )
    parser.add_argument("--C", type=float, default=1.0)
    parser.add_argument(
        "--penalty",
        type=str,
        default="l2",
        choices=["l1", "l2", "elasticnet", "none"],
    )
    parser.add_argument("--solver", type=str, default="lbfgs")

    args = parser.parse_args()
    return TrainConfig(
        input_csv=Path(args.input_csv),
        output_model=Path(args.output_model),
        version=args.version,
        C=args.C,
        penalty=args.penalty,
        solver=args.solver,
    )


if __name__ == "__main__":
    cfg = parse_args()
    train_and_save(cfg)
