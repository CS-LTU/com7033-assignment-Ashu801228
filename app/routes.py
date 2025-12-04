#===========================================================================
#Routes module for the Stroke Risk Prediction web application.

#This file defines:
# Authentication routes (login, logout)
#The main dashboard
# CRUD operations for Patient records
# Views that use the trained ML model to display stroke-risk predictions
#=========================================================================
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
)
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user,
)

from .models import User, Patient
from .forms import LoginForm, PatientForm
from . import db
from .ml import predict_for_patient
from .mongo_db import get_patients_collection

main_bp = Blueprint("main", __name__)


# ---------------------------
# Root -> redirect to login
# ---------------------------
@main_bp.route("/")
def index():
    
    #Root route.
    #If user is logged in, go to dashboard,
    #otherwise go to login page.

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("main.login"))


# ---------------------------
# Login / Logout
# ---------------------------
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page. Uses LoginForm.
    Expects login.html to receive a `form` variable.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid username or password", "danger")

    # IMPORTANT: `form` is always passed to the template
    return render_template("login.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    """
    Log the current user out and return to login page.
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.login"))


# ---------------------------
# Dashboard
# ---------------------------
@main_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Simple dashboard showing counts of total patients and
    those with stroke label = 1.
    Uses only the SQL (SQLite) database.
    """
    total_patients = Patient.query.count()
    stroke_patients = Patient.query.filter_by(stroke=1).count()

    return render_template(
        "dashboard.html",
        total_patients=total_patients,
        stroke_patients=stroke_patients,
    )


# ---------------------------
# List Patients (SQL)
# ---------------------------
@main_bp.route("/patients")
@login_required
def patients_list():
    """
    List all patients from the SQL database.
    """
    patients = Patient.query.order_by(Patient.id.asc()).all()
    return render_template("patients_list.html", patients=patients)


# ---------------------------
# Create Patient (SQL + Mongo)
# ---------------------------
@main_bp.route("/patients/new", methods=["GET", "POST"])
@login_required
def create_patient():
    """
    Create a new patient in SQLite and mirror into MongoDB.
    """
    form = PatientForm()

    if form.validate_on_submit():
        # Create SQL record
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
        )

        # Handle stroke label from form (may be "", "0" or "1")
        if form.stroke.data in (None, "", "None"):
            patient.stroke = None
        else:
            patient.stroke = int(form.stroke.data)

        db.session.add(patient)
        db.session.commit()

        coll = get_patients_collection()
        if coll is not None:
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



# ---------------------------
# Patient Detail + Prediction
# ---------------------------
@main_bp.route("/patients/<int:patient_id>")
@login_required
def patient_detail(patient_id):
    """
    Show patient details from SQL and a stroke prediction
    using the ML model.
    """
    patient = Patient.query.get_or_404(patient_id)

    prediction = None
    try:
        prediction = predict_for_patient(patient)
        # prediction can be a dict like:
        # {"probability": 0.87, "label": 1}
    except Exception:
        # If ML fails for some reason, we just skip prediction
        prediction = None

    return render_template(
        "patient_detail.html",
        patient=patient,
        prediction=prediction,
    )


# ---------------------------
# Edit Patient (SQL + Mongo)
# ---------------------------
@main_bp.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(patient_id):
    """
    Edit an existing patient and sync changes to MongoDB.
    """
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=patient)

    if form.validate_on_submit():
        form.populate_obj(patient)

        if form.stroke.data in (None, "", "None"):
            patient.stroke = None
        else:
            patient.stroke = int(form.stroke.data)

        db.session.commit()

        
        coll = get_patients_collection()
        if coll is not None:
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



# ---------------------------
# Delete Patient (SQL + Mongo)
# ---------------------------
@main_bp.route("/patients/<int:patient_id>/delete", methods=["POST"])
@login_required
def delete_patient(patient_id):
    """
    Delete a patient from SQLite and from MongoDB.
    """
    patient = Patient.query.get_or_404(patient_id)

    # Delete from SQLite
    db.session.delete(patient)
    db.session.commit()

    # Delete from MongoDB
    coll = get_patients_collection()
    coll.delete_one({"sql_id": patient_id})

   


# ---------------------------
# Mongo Patients View
# ---------------------------
@main_bp.route("/mongo-patients")
@login_required
def mongo_patients():
    """
    Display patients from MongoDB.
    MongoDB is required, so any connection problem should raise an error.
    """
    coll = get_patients_collection()
    patients = list(coll.find().sort("sql_id", 1))

    return render_template("mongo_patients.html", patients=patients)
