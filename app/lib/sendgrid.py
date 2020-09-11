from __future__ import annotations
from typing import List, Optional
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from http.client import HTTPResponse
from ssl import SSLContext
import json
import re


class ContentType:
    HTML = "text/html"
    TEXT = "text/plain"


class PersonalizationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class SendGrid:
    SEND_URL = "https://api.sendgrid.com/v3/mail/send"

    def __init__(self, auth_token):
        self.auth_token = auth_token

    @staticmethod
    def create_message(sender, reply_to=None):
        if isinstance(sender, str):
            sender = SendGridMessagePersonalization._parse_address(sender)
        if reply_to and isinstance(reply_to, str):
            reply_to = SendGridMessagePersonalization._parse_address(reply_to)
        return Message(sender, reply_to)

    def send(self, message):

        body = message._prepare_body()
        print(body)
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        req = Request(self.SEND_URL, data=body, headers=headers)
        try:
            response = urlopen(req, context=SSLContext())
            return SendGridResponse.from_http_response(response)
        except HTTPError as err:
            return SendGridResponse.from_http_response(err)


class SendGridMessagePersonalization:
    def __init__(
        self, subject: str, to: list = None, cc: list = None, bcc: list = None
    ):
        self.subject = subject
        self.to = to
        self.cc = cc
        self.bcc = bcc

    @property
    def data(self):
        return {k: v for k, v in self.__dict__.items() if v and not k.startswith("_")}

    @staticmethod
    def _parse_address(address: str):
        patterns = {
            "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
            "name": r"((\'[^\']*\')|(\"[^\"]*\")|([^\s<]+))",
        }

        return {
            k: re.search(regexp, address).group(0) for k, regexp in patterns.items()
        }

    def add_recipient(self, recipient: Optional[str, dict], recipient_type: str):
        if recipient_type not in ["to", "cc", "bcc"]:
            raise PersonalizationError("invalid recipient_type")
        if isinstance(recipient, str):
            recipient = self._parse_address(recipient)
        if self.__dict__[recipient_type] is None:
            self.__dict__[recipient_type] = []
        self.__dict__[recipient_type].append(recipient)

    def __repr__(self):
        attrs = ", ".join(
            [f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_")]
        )
        return f"{self.__class__.__name__}({attrs})"


class SendGridResponse:
    def __init__(self, url, headers, msg, status, reason, length):
        self.url = url
        self.headers = headers
        self.msg = msg
        self.status = status
        self.reason = reason
        self.length = length

    @staticmethod
    def from_http_response(resp: HTTPResponse) -> SendGridResponse:
        headers = {h[0]: h[1] for h in resp.headers}

        return SendGridResponse(
            headers, resp.url, resp.msg, resp.status, resp.reason, resp.length
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.status}>"

    def __bool__(self):
        return self.ok

    @property
    def ok(self):
        return True if self.status < 400 else False


class Message:
    def __init__(
        self,
        send_from: dict,
        reply_to: dict = None,
        content: dict = None,
        personalizations: dict = None,
    ):
        self.send_from = send_from
        self.reply_to = reply_to
        self._content = content if content else {}
        self.personalizations = personalizations if personalizations else {}

    def _prepare_body(self):
        content = [{"type": k, "value": v} for k, v in self.content.items()]

        body = {
            "personalizations": [p.data for p in self.personalizations.values()],
            "from": {"email": self.send_from["email"], "name": self.send_from["name"]},
            "content": sorted(content, key=lambda x: x["type"], reverse=True),
        }
        return json.dumps(body).encode("utf8")

    def add_personalization(self, subject: str, **kwargs):
        personalization = SendGridMessagePersonalization(subject)

        for recipient_type, recipients in kwargs.items():
            if isinstance(recipients, list):
                for recipient in recipients:
                    personalization.add_recipient(recipient, recipient_type)
            elif isinstance(recipients, (str, dict)):
                personalization.add_recipient(recipients, recipient_type)
        self.personalizations[subject] = personalization

    @property
    def content(self):
        return self._content

    def set_content(self, content_type: str, content: str):
        self._content[content_type] = content
