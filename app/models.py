from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Helper table for many-to-many relationship between Doctors and Specialties
_doctor_specialties = db.Table(
    "_doctor_specialties",
    db.Column("doctor_id", db.Integer, db.ForeignKey("doctors.id")),
    db.Column("specialty_id", db.Integer, db.ForeignKey("specialties.id")),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    # NOTE: we use String(2000) because password hashes can be extremely large.
    password = db.Column(db.String(2000), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # patient, doctor, admin

    # Relationships
    patient = db.relationship("Patient", backref="user", uselist=False)
    doctor = db.relationship("Doctor", backref="user", uselist=False)


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    # Relationships
    medical_records = db.relationship("MedicalRecord", backref="patient")
    appointments = db.relationship("Appointment", backref="patient")


class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bio = db.Column(db.Text)

    # Relationships
    specialties = db.relationship(
        "Specialty", secondary=_doctor_specialties, backref="doctors"
    )
    appointments = db.relationship("Appointment", backref="doctor")
    schedules = db.relationship("Schedule", backref="doctor")


class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.String(20), default="scheduled"
    )  # scheduled, canceled, completed
    reason = db.Column(db.Text)


class MedicalRecord(db.Model):
    __tablename__ = "medical_records"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    history = db.Column(db.Text)
    current_case = db.Column(db.Text)
    report = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)


class ResearchProject(db.Model):
    __tablename__ = "research_projects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="active")  # active, completed, paused
    lead_researcher_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)


class Document(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    document_type = db.Column(db.String(50))  # personal, clinical
    filename = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.now)


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.now)


class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), default="unread")  # unread, read
    created_at = db.Column(db.DateTime, default=datetime.now)


class Specialty(db.Model):
    __tablename__ = "specialties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    day_of_week = db.Column(db.String(20))  # Monday, Tuesday, etc.
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)


class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, default=datetime.now)
    status = db.Column(db.String(20))  # present, absent
    justification = db.Column(db.Text)
