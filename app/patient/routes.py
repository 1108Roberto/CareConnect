from flask import Blueprint, abort, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Appointment, db
from app.forms import AppointmentForm

bp = Blueprint("patient", __name__, url_prefix="/patient")


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("patient/dashboard.html")


@bp.route("/appointments")
@login_required
def appointments():
    appointments = current_user.patient_profile.appointments
    return render_template("patient/appointments.html", appointments=appointments)


@bp.route("/appointments/new", methods=["GET", "POST"])
@login_required
def new_appointment():
    form = AppointmentForm()

    # Populate doctors (simple implementation)
    form.doctor.choices = [(d.id, d.user.username) for d in Doctor.query.all()]

    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=current_user.patient_profile.id,
            doctor_id=form.doctor.data,
            scheduled_time=form.scheduled_time.data,
            reason=form.reason.data,
            status="Requested",
        )
        db.session.add(appointment)
        db.session.commit()
        flash("Appointment requested!")
        return redirect(url_for("patient.appointments"))

    return render_template("patient/new_appointment.html", form=form)


@bp.route("/appointments/<int:id>/cancel")
@login_required
def cancel_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.patient_id != current_user.patient_profile.id:
        abort(403)

    appointment.status = "Canceled"
    db.session.commit()
    flash("Appointment canceled")
    return redirect(url_for("patient.appointments"))


@bp.route("/account")
@login_required
def account_status():
    payments = current_user.patient_profile.payments
    return render_template("patient/account.html", payments=payments)


@bp.route("/documents")
@login_required
def documents():
    docs = current_user.documents
    return render_template("patient/documents.html", documents=docs)
