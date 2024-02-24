import os

from flask import Flask, session

from api.home_bp import home_bp
from api.about_bp import about_bp
from api.auth_bp import auth_bp
from models import db, User

app = Flask(__name__)

app.secret_key = "super secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pigeon-hole.db"

app.app_context().push()

db.init_app(app)
db.create_all()

app.register_blueprint(home_bp, url_prefix="/")
app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)
