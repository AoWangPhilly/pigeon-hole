import os

from flask import Flask, session

from api.home_bp import home_bp
from api.about_bp import about_bp
from api.auth_bp import auth_bp
from api.pigeon_bp import pigeon_bp
from dotenv import load_dotenv

from models import db, User

load_dotenv()
app = Flask(__name__)

app.secret_key = str(os.getenv("SECRET_KEY"))
app.config["SQLALCHEMY_DATABASE_URI"] = str(os.getenv("POSTGRES_URL"))

app.app_context().push()

db.init_app(app)
db.create_all()

app.register_blueprint(home_bp, url_prefix="/")
app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(pigeon_bp, url_prefix="/pigeon")

if __name__ == "__main__":
    app.run(debug=True)
