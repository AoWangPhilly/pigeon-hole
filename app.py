# app.py
from flask import Flask
from api.home_bp import home_bp
from api.about_bp import about_bp
from api.auth_bp import auth_bp
from database import init_db

app = Flask(__name__)

init_db()
app.register_blueprint(home_bp, url_prefix="/")
app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)
