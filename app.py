import os

from dotenv import load_dotenv
from flask import Flask

from api.home_bp import home_bp
from api.about_bp import about_bp
from api.auth_bp import auth_bp
from api.pigeon_bp import pigeon_bp
from api.hierarchy_bp import hierarchy_bp
from cache import cache
from models import db


load_dotenv()
app = Flask(__name__, static_folder="static", template_folder="templates")

app.secret_key = str(os.getenv("SECRET_KEY"))
app.config["SQLALCHEMY_DATABASE_URI"] = str(os.getenv("POSTGRES_URL")).replace(
    "postgres://", "postgresql://"
)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

cache.init_app(
    app,
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": "cache",
        "CACHE_THRESHOLD": 100_000,
    },
)

app.app_context().push()

db.init_app(app)
db.create_all()

app.register_blueprint(home_bp, url_prefix="/")
app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(pigeon_bp, url_prefix="/pigeon")
app.register_blueprint(hierarchy_bp, url_prefix="/hierarchy")

if __name__ == "__main__":
    app.run(debug=True)
