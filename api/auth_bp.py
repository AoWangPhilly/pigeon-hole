from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    request,
    jsonify,
)
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

from models import User, db
from forms import RegisterForm, LoginForm


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        try:
            user = User(
                email=form.email.data,
                password=pbkdf2_sha256.hash(form.password.data),
                name=f"{form.first_name.data} {form.last_name.data}",
            )
            db.session.add(user)
            db.session.commit()
            session["user"] = user
            return redirect("/")
        except SQLAlchemyError as e:
            db.session.rollback()
            return render_template(
                "register.html",
                form=form,
            )
    return render_template(
        "register.html",
        form=form,
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        session["user"] = user
        return redirect("/"), 302
    return render_template("login.html", form=form), 200


@auth_bp.route("/get-user")
def get_users():
    return jsonify(User.query.all())
