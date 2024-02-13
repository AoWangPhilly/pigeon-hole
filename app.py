from flask import Flask
from api.home import home

app = Flask(__name__)

# Register the blueprint with the app
app.register_blueprint(home)

if __name__ == "__main__":
    app.run(debug=True)
