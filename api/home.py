from flask import Blueprint, render_template

# Create a Blueprint named 'my_blueprint'
home = Blueprint(
    "home",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# Define a route within the Blueprint
@home.route("/")
def hello():
    return render_template("home.html")
