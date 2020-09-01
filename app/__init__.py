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
        "MAIL_PASSWORD": os.getenv("MAIL_PASSWORD"),
    }

    app.config.update(settings)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html"), 200

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return render_template("405.html"), 405

    @app.errorhandler(500)
    def not_found(error):
        return render_template("500.html"), 500

    return app


if __name__ == "__main__":
    app = create_app()

    app.run()