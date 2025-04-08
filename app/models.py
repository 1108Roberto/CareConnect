from datetime import datetime
from typing import AnyStr, Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(
        Enum("Patient", "Doctor", "Admin", name="user_roles"), nullable=False
    )

    # Relationships
    patient_profile = db.relationship(
        "Patient", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    doctor_profile = db.relationship(
        "Doctor", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    documents = db.relationship("Document", back_populates="user")
    alerts = db.relationship("Alert", back_populates="user")

    def set_password(self, password: Optional[AnyStr]):
        # TEMPORARY: Store plain text (replace with hashing later)
        self.password = password

    def check_password(self, password: Optional[AnyStr]):
        # TEMPORARY: Plain text comparison
        return self.password == password


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(200))
    emergency_contact = db.Column(db.String(100))

    user = db.relationship("User", back_populates="patient_profile")
    appointments = db.relationship("Appointment", back_populates="patient")
    medical_records = db.relationship("MedicalRecord", back_populates="patient")
    payments = db.relationship("Payment", back_populates="patient")


class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    license_number = db.Column(db.String(50), unique=True)
    specialty_id = db.Column(db.Integer, db.ForeignKey("specialties.id"))

    user = db.relationship("User", back_populates="doctor_profile")
    specialty = db.relationship("Specialty", back_populates="doctors")
    appointments = db.relationship("Appointment", back_populates="doctor")
    schedules = db.relationship("Schedule", back_populates="doctor")


class Specialty(db.Model):
    __tablename__ = "specialties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    doctors = db.relationship("Doctor", back_populates="specialty")


class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        Enum(
            "Requested", "Confirmed", "Canceled", "Completed", name="appointment_status"
        )
    )
    reason = db.Column(db.Text)

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")


class MedicalRecord(db.Model):
    __tablename__ = "medical_records"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    patient = db.relationship("Patient", back_populates="medical_records")


class Document(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    document_type = db.Column(
        Enum("Prescription", "Lab_Result", "ID", "Insurance", name="document_types")
    )
    file_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User", back_populates="documents")


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(Enum("Pending", "Completed", "Refunded", name="payment_status"))
    transaction_date = db.Column(db.DateTime, default=datetime.now)

    patient = db.relationship("Patient", back_populates="payments")


class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(Enum("Unread", "Read", name="alert_status"))
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User", back_populates="alerts")


class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    doctor = db.relationship("Doctor", back_populates="schedules")


class ResearchProject(db.Model):
    __tablename__ = "research_projects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(Enum("Active", "Completed", "On_Hold", name="project_status"))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
