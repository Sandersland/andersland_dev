from flask import Blueprint, current_app, request, jsonify, render_template


from app.lib.sendgrid import SendGrid, ContentType

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
    sendgrid_key = config.get("SENDGRID_API_KEY")

    keys = ["email", "name", "subject", "message"]
    values = [data.get(key) for key in keys]
    if not all(values):
        response["status"] = "error"
        response["message"] = "Bad Request"
        return jsonify(response), 400

    message = SendGrid.create_message(f"'andersland.dev' <{username}>", reply_to)
    message.set_content(
        ContentType.TEXT,
        f"Hello {data['name']}, thank you for your message! I'll be in touch!",
    )
    message.add_personalization(
        subject=data["subject"],
        to=f"'{data['name']}' <{data['email']}>",
        bcc=username,
    )

    with current_app.app_context():
        message.set_content(
            ContentType.HTML, render_template("mail/notify.html", **data)
        )

    sg = SendGrid(sendgrid_key)
    sg_resp = sg.send(message)
    if not sg_resp.ok:
        response["status"] = "error"
        response["message"] = sg_resp.reason
        return jsonify(response), 500

    response["status"] = "success"
    response["message"] = "Your message was successfully sent."
    return jsonify(response), 200
