import os

from app import create_app

settings = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "MAIL_USERNAME": os.getenv("MAIL_USERNAME"),
    "MAIL_REPLY_TO": os.getenv("MAIL_REPLY_TO"),
    "SENDGRID_API_KEY": os.getenv("SENDGRID_API_KEY"),
}

app = create_app(settings)

if __name__ == "__main__":
    app.run()