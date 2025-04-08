from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeLocalField, SubmitField, TextAreaField


class AppointmentForm(FlaskForm):
    doctor = SelectField("Doctor", coerce=int)
    scheduled_time = DateTimeLocalField("Date/Time", format="%Y-%m-%dT%H:%M")
    reason = TextAreaField("Reason")
    submit = SubmitField("Request Appointment")
