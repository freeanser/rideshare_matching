# backend/app.py

from flask import Flask
from flask_cors import CORS
from controllers.admin import admin_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # register blueprints
    app.register_blueprint(admin_bp)

    # define index route HERE
    @app.route("/")
    def index():
        return "Backend is running!"

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
