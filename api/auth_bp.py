from flask import Blueprint, render_template, session, redirect, request, jsonify, Response

from models import User, db

from passlib.hash import pbkdf2_sha256

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


@auth_bp.route("/register", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        return render_template("register.html", error=None), 200

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not all((first_name, last_name, email, password)):
        return render_template("register.html", error="All fields are required"), 400

    if db.session.query(User).filter_by(email=email).first() is not None:
        return render_template("register.html", error="Email already in use"), 400

    encrypted_password = pbkdf2_sha256.hash(password)
    user = User(email=email, password=encrypted_password, name=f"{first_name} {last_name}")
    db.session.add(user)
    db.session.commit()

    return redirect("/auth/login"), 201

@auth_bp.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "GET":
        return render_template("login.html"), 200

    email = request.form.get("email")
    password = request.form.get("password")

    if not all((email, password)):
        return render_template("login.html", error="All fields are required"), 400

    user = db.session.query(User).filter_by(email=email).first()

    if user is None:
        return render_template("login.html", error="Invalid email address"), 400

    if not pbkdf2_sha256.verify(password, user.password):
        return render_template("login.html", error="Invalid password"), 400

    session["user"] = user
    return redirect("/"), 200


@auth_bp.route("/get-user")
def get_users():
    return jsonify(User.query.all())
