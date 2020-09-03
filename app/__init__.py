from flask import Flask, render_template


def create_app(settings):
    from app.api import api_bp

    app = Flask(__name__)

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
