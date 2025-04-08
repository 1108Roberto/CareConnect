from flask import Flask, render_template, request, redirect
from app.models import db, User
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        new_user = User(email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return f"Logged in as {user.role}"
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
