#===========================================================================
#Routes module for the Stroke Risk Prediction web application.

#This file defines:
# Authentication routes (login, logout)
#The main dashboard
# CRUD operations for Patient records
# Views that use the trained ML model to display stroke-risk predictions
#=========================================================================
from .mongo_db import get_patients_collection
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from .models import User, Patient
from .forms import LoginForm, PatientForm
from . import db
from .ml import predict_for_patient

main_bp = Blueprint("main", __name__)


# ---------------------------
# Login
# ---------------------------
@main_bp.route("/", methods=["GET", "POST"])
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.dashboard"))
        flash("Invalid username or password", "danger")

    #  pass form to template
    return render_template("login.html", form=form)


# ---------------------------
# Logout
# ---------------------------
@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.login"))


# ---------------------------
# Dashboard
# ---------------------------
@main_bp.route("/dashboard")
@login_required
def dashboard():
    total_patients = Patient.query.count()
    stroke_count = Patient.query.filter_by(stroke=1).count()

    return render_template(
        "dashboard.html",
        total_patients=total_patients,
        stroke_count=stroke_count,
    )


# ---------------------------
# List Patients
# ---------------------------
@main_bp.route("/patients")
@login_required
def patients_list():
    patients = Patient.query.order_by(Patient.id.asc()).all()
    return render_template("patients_list.html", patients=patients)


# ---------------------------
# Patient Details + Stroke Prediction
# ---------------------------
@main_bp.route("/patients/<int:patient_id>")
@login_required
def patient_detail(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    prediction = None
    try:
        proba, label = predict_for_patient(patient)
        prediction = (proba, label)
    except Exception as e:
        flash(f"Prediction error: {e}", "warning")

    return render_template(
        "patient_detail.html",
        patient=patient,
        prediction=prediction,
    )


# ---------------------------
# Create Patient
# ---------------------------
@main_bp.route("/patients/new", methods=["GET", "POST"])
@login_required
def create_patient():
    form = PatientForm()

    if form.validate_on_submit():
        patient = Patient(
            gender=form.gender.data,
            age=form.age.data,
            hypertension=form.hypertension.data,
            heart_disease=form.heart_disease.data,
            ever_married=form.ever_married.data,
            work_type=form.work_type.data,
            residence_type=form.residence_type.data,
            avg_glucose_level=form.avg_glucose_level.data,
            bmi=form.bmi.data,
            smoking_status=form.smoking_status.data,
            stroke=form.stroke.data,
        )
        db.session.add(patient)
        db.session.commit()
         # Also insert into MongoDB as a document
        coll = get_patients_collection()
        coll.insert_one({
            "sql_id": patient.id,
            "gender": patient.gender,
            "age": patient.age,
            "hypertension": patient.hypertension,
            "heart_disease": patient.heart_disease,
            "ever_married": patient.ever_married,
            "work_type": patient.work_type,
            "residence_type": patient.residence_type,
            "avg_glucose_level": patient.avg_glucose_level,
            "bmi": patient.bmi,
            "smoking_status": patient.smoking_status,
            "stroke": patient.stroke,
        })
        flash("Patient created successfully.", "success")
        return redirect(url_for("main.patients_list"))

    #  pass form
    return render_template("patient_form.html", form=form, title="Create Patient")


# ---------------------------
# Edit Patient
# ---------------------------
@main_bp.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=patient)

    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.commit()
        # Sync changes to MongoDB
        coll = get_patients_collection()
        coll.update_one(
            {"sql_id": patient.id},
            {"$set": {
                "gender": patient.gender,
                "age": patient.age,
                "hypertension": patient.hypertension,
                "heart_disease": patient.heart_disease,
                "ever_married": patient.ever_married,
                "work_type": patient.work_type,
                "residence_type": patient.residence_type,
                "avg_glucose_level": patient.avg_glucose_level,
                "bmi": patient.bmi,
                "smoking_status": patient.smoking_status,
                "stroke": patient.stroke,
            }},
            upsert=True,
        )
        flash("Patient updated successfully.", "success")
        return redirect(url_for("main.patient_detail", patient_id=patient.id))

    #  pass form
    return render_template("patient_form.html", form=form, title="Edit Patient")


# ---------------------------
# Delete Patient
# ---------------------------
@main_bp.route("/patients/<int:patient_id>/delete", methods=["POST"])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    # Delete from SQLite
    db.session.delete(patient)
    db.session.commit()

    # Delete from MongoDB
    coll = get_patients_collection()
    coll.delete_one({"sql_id": patient_id})

    flash("Patient deleted successfully from SQL and MongoDB.", "info")
    return redirect(url_for("main.patients_list"))
