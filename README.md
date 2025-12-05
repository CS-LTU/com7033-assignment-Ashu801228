#==============================================================================================================================================================
										  COM7303 - SECURE SOFTWARE DEVELOPMENT 
	                                      
										  STROKE RISK WEB APPLICATION - SUBMISSION 
										  
										      ASHU MATHIAS ASHU 
										      LEEDS TRINITY UNIVERSITY 
		
#==============================================================================================================================================================
                                       


                                               TABLE  OF  CONTENTS

1. Abstract

2.	Introduction

3.	Features Overview

4.	System Architecture

5.	Multi-Database Design (SQLite + MongoDB)

6.	Security Design & Practices

7.	Machine Learning Component

8.	Installation Instructions

9.	Database Setup

10.	Running the Application

11.	Testing Strategy

12.	The Web Application Structure

13.	Limitations

14.	Future Enhancements
                                                                        
15.	Conclusion

16.	Acknowledgement 


                                                  1.  ABSTRACT 
												  
This report  presents a secure, multi-database Flask web application designed for managing stroke-related patient
information and supporting stroke prediction using a Logistic Regression machine learning model. The application
integrates two distinct database systems namely SQLite for structured relational storage; and MongoDB for flexible NoSQL 
document storage—to demonstrate multi-database architecture. Key security practices, including password hashing,
CSRF protection, secure session handling, and input validation, ensure safe data processing. This README  serves 
as both the technical documentation and the written report for the coursework assessment.
												  
                                                   2. INTRODUCTION 

Stroke is one of the leading global health issues, and early detection is crucial for effective intervention. 
This report focuses on developing a secure Flask web application that manages stroke patient data 
and predicts stroke risk using a machine learning model.
The application demonstrates:Secure programming practices,Proper use of relational (SQLite) and non-relational (MongoDB) databases,
Full CRUD functionality for patient records,Authentication and session security,Integration of a trained Logistic Regression model for stroke prediction and 
Effective use of GitHub version control with multiple meaningful commits.
By embedding this report within the README, the Wep Application  meets the assessment requirement for a written technical
explanation while maintaining accessibility for readers.


                                                    3. FEATURES OVERVIEW 
													
													
Secure login system with hashed passwords.

Manage patient records (Create, Read, Update, Delete)

Import stroke dataset into SQLite.

Mirror patient records into MongoDB.

Display SQL and MongoDB patient data.

Predict stroke risk using a trained ML model.

Error logging for debugging.

Unit tests for authentication and configuration.

Professional UI templates with clean navigation.


                                                       4. SYSTEM ARCHITECTURE
													   

The application follows the Flask Blueprint architecture:

run.py → Creates Flask app → Registers Blueprint.
app/
 ├── __init__.py (app factory, DB setup, login manager)
 ├── routes.py (main views)
 ├── models.py (SQLAlchemy models)
 ├── forms.py (WTForms validation)
 ├── config.py (secure settings)
 └── ml.py (prediction logic)

Key Architectural Choices.

Separation of concerns (routes, models, config, forms)

App factory pattern for scalability.

Independent databases for both security and clarity.

MongoDB mirroring ensures redundancy and flexibility.


                                                        5. MULTI-DATABASE DESIGN
															
															

The application uses two active databases,namely:

1. 
a.	SQLite (auth.db)-Stores user accounts and hashed passwords
b.	SQLite (patients.db)Stores structured patient medical data.Created dynamically after importing CSV or adding new patients.

2. MongoDB (NoSQL)

Stores patient documents structured as JSON-like objects.
Used for flexible retrieval and modern database demonstration.

The application  uses both SQL and NoSQL. Reasons:

SQL handles relational, structured data with integrity constraints.

NoSQL offers document flexibility and is ideal for mirroring or analytics.


                                                         6. SECURITY DESIGN & PRACTICES 

The following security techniques were implemented:

A.	Password Hashing

Using Werkzeug’s generate_password_hash and check_password_hash.

B.	CSRF Protection

Every form includes a hidden CSRF token via Flask-WTF.

C.	Secure Sessions

Settings include:

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = 'Lax'

D.	Input Validation

WTForms ensures strict type validation and sanitisation.

F.	 Error Logging

Errors recorded in logs/app.log without leaking sensitive data.

✔ Database Safety

All SQL queries use SQLAlchemy ORM — no raw string SQL.


                                                          7. MACHINE LEARNING COMPONENT
																	  
																	  

A Logistic Regression model is trained using the following attributes of the given stroke -prediction dataset:

age
hypertension
heart disease
glucose
BMI
smoking status
The training script:
scripts/train_model.py

produces:

models/stroke_model.joblib.This model is loaded by app/ml.py and used to:
Generate predictions for new patients
Display stroke risk status in the UI
The ML integration demonstrates applied data science within a secure web application.


                                                             8. INSTALLATION INSTRUCTIONS 
																		   
																		   
git clone https://github.com/CS-LTU/com7033-assignment-Ashu801228.git
cd C:\Users\HP\stroke-risk-app
conda create -n strokeenv python=3.11
conda activate strokeenv
pip install -r requirements.txt

                                                             9. DATABASE SETUP
																		   
																		   
Import the stroke dataset:
python scripts/import_patients.py
Start MongoDB:
net start MongoDB
Ensure MongoDB Compass or the default service is installed.

                                                              10. RUNNING THE APPLICATION
																		   
																		   
python run.py
Open in browser:
http://127.0.0.1:5000
Login Credentials (for demonstration)
Username: admin
Password: admin123



                                                                11. TESTING STRATEGY 

Unit tests located in:
tests/
Run:
pytest produces the follow result:

================================================= test session starts =================================================
platform win32 -- Python 3.11.14, pytest-9.0.1, pluggy-1.6.0
rootdir: C:\Users\HP\stroke-risk-app
collected 3 items

tests\test_auth.py ..                                                                                            [ 66%]
tests\test_config.py .                                                                                           [100%]

================================================== 3 passed in 2.09s ==================================================

Tests cover:

Authentication with hashed passwords

Config security settings

Application creation

                                                               12.THE  WEB APPLICATION  STRUCTURE 
stroke-risk-app/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── config.py
│   └── ml.py
├── data/
│   └── patients.csv
├── instance/
│   ├── auth.db
│   └── patients.db
├── models/
│   └── stroke_model.joblib
├── scripts/
│   ├── import_patients.py
│   └── train_model.py
├── templates/
├── static/
├── tests/
├── run.py
└── README.md


                                                               13. LIMITATIONS 
															   
															   

Small dataset limits ML accuracy

No role-based access control (admin/doctor/nurse)

Single admin account

No password reset or email verification



                                                                 14. Future Enhancements

Add user roles with permissions

Improve ML pipeline (scaling, hyperparameter tuning)

Add data analytics dashboards

Docker containerisation

REST API endpoints for mobile integration

                                                                   15. CONCLUSION 


This report demonstrates a secure, well-structured, and fully functional Flask application
integrating multiple databases, machine learning, and comprehensive security practices.
The system provides  functionality and documentation,
and the version control history gives clear evidence of development progress.

                                                                    16. ACKNOWLEDGEMENET 
																	
This Web Application  makes use of some standard python codes from the course sessions. 
This assignment used AI tool for the purposes of editing relevant python codes.  

                                                                 
                    
                           