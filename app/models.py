from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Patient(db.Model):
    __bind_key__ = "patients"  # <-- This model uses patients.db
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(20))
    age = db.Column(db.Float)
    hypertension = db.Column(db.Boolean, default=False)
    heart_disease = db.Column(db.Boolean, default=False)
    ever_married = db.Column(db.String(10))
    work_type = db.Column(db.String(50))
    residence_type = db.Column(db.String(20))
    avg_glucose_level = db.Column(db.Float)
    bmi = db.Column(db.Float)
    smoking_status = db.Column(db.String(50))
    stroke = db.Column(db.Boolean, default=False)  # label in dataset

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
