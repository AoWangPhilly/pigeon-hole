from flask import Blueprint, render_template

pigeon_bp = Blueprint(
    "pigeon",
    __name__,
)


@pigeon_bp.route("/view")
def view():
    return render_template("view.html")
