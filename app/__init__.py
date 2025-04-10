from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app.models import *
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# Role checker
def role_required(role):
    def decorator(f):
        @wraps(f)  # type: ignore[reportUnknownArgumentType]
        def wrapped(*args, **kwargs):
            if not session.get("role") == role:
                return redirect(url_for("login"))
            return f(*args, **kwargs)

        return wrapped

    return decorator


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Simple validation
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Missing credentials", 400

        if User.query.filter_by(email=email).first():
            return "Email exists", 400

        # Create user with hashed password
        new_user = User(
            email=email,
            password=generate_password_hash(password),
            role="patient",  # Only patient self-registration
        )

        db.session.add(new_user)
        db.session.commit()

        # Create patient profile
        patient = Patient(user_id=new_user.id)
        db.session.add(patient)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()

        if user and check_password_hash(user.password, request.form.get("password")):  # type: ignore
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect(f"/{user.role}_dashboard")

        return "Invalid login", 401

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/patient_dashboard")
@role_required("patient")
def patient_dashboard():
    return "Patient Dashboard - <a href='/logout'>Logout</a>"


@app.route("/doctor_dashboard")
@role_required("doctor")
def doctor_dashboard():
    return "Doctor Dashboard - <a href='/logout'>Logout</a>"


@app.route("/admin_dashboard")
@role_required("admin")
def admin_dashboard():
    return "Admin Dashboard - <a href='/logout'>Logout</a>"


if __name__ == "__main__":
    app.run(debug=True)
