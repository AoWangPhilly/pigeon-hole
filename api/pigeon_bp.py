from flask import Blueprint, render_template, request

pigeon_bp = Blueprint(
    "pigeon",
    __name__,
)


@pigeon_bp.route("/view")
def view():
    return render_template("view.html")

@pigeon_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
