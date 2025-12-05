#=========================================================================
#Forms module for the Stroke Risk Prediction web application.

#This file defines:
# LoginForm: handles user authentication input with validation
# PatientForm: handles patient data input for create/update operations
# including validation rules to ensure data integrity.

#Flask-WTF is used for:
# CSRF protection (automatically added via hidden_tag)
#Input validation (DataRequired, NumberRange, Length, Optional)
#==========================================================================

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    FloatField,
    BooleanField,
    SelectField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    NumberRange,
    Length,
    Optional,
)
# -------------------------
# User Authentication Form
# -------------------------

class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(max=80)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )
    submit = SubmitField("Login")
# ------------------------------------------
# Patient Data Entry Form
# Used for adding and editing patient records
# -------------------------------------------
class PatientForm(FlaskForm):

    gender = SelectField(
        "Gender",
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        validators=[DataRequired()],
    )
    age = IntegerField(
        "Age",
        validators=[DataRequired(), NumberRange(min=0, max=120)],
    )
    hypertension = SelectField(
        "Hypertension",
        choices=[("0", "No"), ("1", "Yes")],
        validators=[DataRequired()],
    )
    heart_disease = SelectField(
        "Heart Disease",
        choices=[("0", "No"), ("1", "Yes")],
        validators=[DataRequired()],
    )
    ever_married = SelectField(
        "Ever Married",
        choices=[("No", "No"), ("Yes", "Yes")],
        validators=[DataRequired()],
    )
    work_type = SelectField(
        "Work Type",
        choices=[
            ("Private", "Private"),
            ("Self-employed", "Self-employed"),
            ("Govt_job", "Government job"),
            ("children", "Children"),
            ("Never_worked", "Never worked"),
        ],
        validators=[DataRequired()],
    )
    residence_type = SelectField(
        "Residence Type",
        choices=[("Urban", "Urban"), ("Rural", "Rural")],
        validators=[DataRequired()],
    )
    avg_glucose_level = FloatField(
        "Average Glucose Level",
        validators=[DataRequired(), NumberRange(min=0)],
    )
    bmi = FloatField(
        "BMI",
        validators=[Optional(), NumberRange(min=0)],
    )
    smoking_status = SelectField(
        "Smoking Status",
        choices=[
            ("formerly smoked", "Formerly smoked"),
            ("never smoked", "Never smoked"),
            ("smokes", "Smokes"),
            ("Unknown", "Unknown"),
        ],
        validators=[DataRequired()],
    )
    stroke = SelectField(
        "Stroke Label",
        choices=[
            ("", "Unknown / Not labelled"),
            ("0", "No stroke (0)"),
            ("1", "Has stroke (1)"),
        ],
        validators=[Optional()],
    )

    submit = SubmitField("Save")

