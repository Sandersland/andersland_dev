import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, current_app, request, jsonify, render_template


api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/message", methods=["POST"])
def message():
    response = {}
    content_type = request.headers.get("Content-Type")
    data = request.json

    if not content_type or content_type != "application/json":
        response["status"] = "error"
        response["message"] = "Bad Request"
        return jsonify(response), 400

    config = current_app.config
    username = config.get("MAIL_USERNAME")
    reply_to = config.get("MAIL_REPLY_TO")
    password = config.get("MAIL_PASSWORD")
    mail_server = config.get("MAIL_SERVER")
    mail_port = config.get("MAIL_PORT")

    keys = ["email", "name", "subject", "message"]
    values = [data.get(key) for key in keys]
    if not all(values):
        response["status"] = "error"
        response["message"] = "Bad Request"
        return jsonify(response), 400

    msg = MIMEMultipart("alternative")
    msg.add_header("reply-to", reply_to)
    msg["Subject"] = "Message confirmation"
    msg["From"] = f"andersland.dev <{username}>"
    msg["To"] = data["email"]
    msg["Bcc"] = reply_to

    text = f"Hello {data['name']}, thank you for your message! I'll be in touch!"
    text_part = MIMEText(text, "plain")
    msg.attach(text_part)

    with current_app.app_context():
        html = render_template("mail/notify.html", **data)
        html_part = MIMEText(html, "html")
        msg.attach(html_part)

    try:
        response["status"] = "success"
        response["message"] = "Your message was successfully sent."
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