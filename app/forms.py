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
# -------------------------
# Patient Data Entry Form
# Used for adding and editing patient records
# -------------------------

class PatientForm(FlaskForm):
    gender = SelectField(
        "Gender",
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other"),
        ],
        validators=[DataRequired()],
    )

    age = IntegerField(
        "Age",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=120),
        ],
    )

    hypertension = BooleanField("Hypertension")
    heart_disease = BooleanField("Heart Disease")

    ever_married = SelectField(
        "Ever married",
        choices=[
            ("Yes", "Yes"),
            ("No", "No"),
        ],
        validators=[DataRequired()],
    )

    work_type = StringField(
        "Work type",
        validators=[
            DataRequired(),
            Length(max=120),
        ],
    )

    residence_type = SelectField(
        "Residence type",
        choices=[
            ("Urban", "Urban"),
            ("Rural", "Rural"),
        ],
        validators=[DataRequired()],
    )

    avg_glucose_level = FloatField(
        "Average glucose level",
        validators=[
            DataRequired(),
            NumberRange(min=0),
        ],
    )

    bmi = FloatField(
        "BMI",
        validators=[
            Optional(),
            NumberRange(min=0),
        ],
    )

    smoking_status = StringField(
        "Smoking status",
        validators=[
            Optional(),
            Length(max=120),
        ],
    )

    # Stroke label as in dataset: 0 = no stroke, 1 = stroke
    stroke = SelectField(
        "Stroke (dataset label)",
        choices=[
            ("0", "0 - No stroke"),
            ("1", "1 - Stroke"),
        ],
        default="0",
        validators=[DataRequired()],
    )

    submit = SubmitField("Save")
