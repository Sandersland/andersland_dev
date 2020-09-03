import os

from app import create_app

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

app = create_app(settings)

if __name__ == "__main__":
    app.run()