from functools import wraps
from flask import render_template, Blueprint
from flask_login import login_required, current_user
from typing import Any

main = Blueprint("main", __name__)


@main.route("/")
def index() -> str:
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard() -> str | Any:
    if current_user.role == "Patient":
        return render_template("patient_dashboard.html")
    elif current_user.role in ["Doctor", "Admin"]:
        return render_template("staff_dashboard.html")
    return redirect(url_for("index"))


@main.route("/about")
def about() -> str:
    return render_template("about.html")


@main.route("/research")
def research() -> str:
    return render_template("research.html")


# Add role checking decorator
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role == role:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
