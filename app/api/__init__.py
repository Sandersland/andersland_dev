import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, current_app, request, jsonify, render_template


api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/message", methods=["POST"])
def message():
    response = {}

    config = current_app.config
    username = config.get("MAIL_USERNAME")
    password = config.get("MAIL_PASSWORD")
    mail_server = config.get("MAIL_SERVER")
    mail_port = config.get("MAIL_PORT")

    data = request.json
    email = data.get("email")
    name = data.get("name")
    subject = data.get("subject")
    message = data.get("message")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"andersland.dev <{username}>"
    msg["To"] = username

    text = f"Thank you, {name}! Thank you for your message. I'll be in touch!"
    text_part = MIMEText(text, "plain")
    msg.attach(text_part)

    with current_app.app_context():
        html = render_template("mail/notify.html", **data)
        html_part = MIMEText(html, "html")
        msg.attach(html_part)

    try:
        response["status"] = "success"
        response["message"] = "email sent successfully"
        server = smtplib.SMTP_SSL(mail_server, mail_port)
        server.ehlo()
        server.login(username, password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.close()
        return jsonify(response), 200

    except Exception as err:
        response["status"] = "error"
        response["message"] = str(err)
        return jsonify(response), 500