import os
import smtplib

from flask import Flask, render_template, jsonify, request


def create_app():
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
        return render_template("index.html")

    @app.route("/message", methods=["POST"])
    def message():
        response = {}
        data = request.json

        subject = f"{data.get('name')} would like to contact you!"
        to = app.config.get("MAIL_USERNAME")
        _from = data.get("name")

        message = f"Subject: {subject}\n\n{data.get('message')}"

        try:
            response["status"] = "success"
            response["message"] = "email sent successfully"
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
            server.login(
                app.config.get("MAIL_USERNAME"), app.config.get("MAIL_PASSWORD")
            )
            server.sendmail(_from, to, message)
            server.close()
            return jsonify(response), 200

        except Exception as err:
            response["status"] = "error"
            response["message"] = str(err)
            return jsonify(response), 500

    return app


if __name__ == "__main__":
    app = create_app()

    app.run()