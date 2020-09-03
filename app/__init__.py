import os
import smtplib

from flask import Flask, render_template, jsonify, request


def create_app():
    from app.api import api_bp

    app = Flask(__name__)

    settings = {
        "SECRET_KEY": os.getenv("SECRET_KEY"),
        "MAIL_SERVER": os.getenv("MAIL_SERVER"),
        "MAIL_PORT": os.getenv("MAIL_PORT"),
        "MAIL_USE_TLS": os.getenv("MAIL_USE_TLS"),
        "MAIL_USE_SSL": os.getenv("MAIL_USE_SSL"),
        "MAIL_USERNAME": os.getenv("MAIL_USERNAME"),
        "MAIL_REPLY_TO": os.getenv("MAIL_REPLY_TO"),
        "MAIL_PASSWORD": os.getenv("MAIL_PASSWORD"),
    }

    app.config.update(settings)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html"), 200

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.errorhandler(404)
    def not_found(error):
        data = {"error": "404", "message": "Not Found"}
        return render_template("error.html", **data), 404

    @app.errorhandler(405)
    def not_allowed(error):
        data = {"error": "405", "message": "Not Allowed"}
        return render_template("error.html", **data), 405

    @app.errorhandler(500)
    def not_found(error):
        data = {"error": "500", "message": "Server Error"}
        return render_template("error.html", **data), 500

    return app


if __name__ == "__main__":
    app = create_app()

    app.run()