from typing import Any, Optional
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug import Response
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User, Patient, Doctor, db

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    form = LoginForm()
    if form.validate_on_submit():
        user: Optional[Any] = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid credentials")
    return render_template("login.html", form=form)


@bp.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("index"))


@bp.route("/register", methods=["GET", "POST"])
def register() -> Response | str:
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role="Patient")  # Default role
        user.set_password(form.password.data)
        db.session.add(user)

        # Create patient profile
        patient = Patient(user=user)
        db.session.add(patient)

        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)
