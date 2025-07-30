import requests
from .groups import Groups
from .teams import Teams


class Pushover:
    def __init__(self, token: str, default_user: str = None):
        self.token = token
        self.Group = Groups(self.token)
        self.default_user = default_user
        self.Teams = Teams()

    def push(self, message: str, user: str = None,
             title: str = None,
             attachment: str = None,
             attachment_base64: str = None,
             attachment_type: str = None,
             device: str = None,
             html: int = 0,
             monospace: int = 0,
             priority: int = 0,
             sound: str = None,
             timestamp: int = None,
             ttl: int = None,
             url: str = None,
             url_title: str = None,
             ):
        user = user or self.default_user
        if not user:
            raise ValueError("User key is required (either as argument or default_user)")

        if priority not in [-2, -1, 0, 1, 2]:
            raise ValueError("Priority must be in (-2, -1, 0, 1, 2)")

        if html not in [0, 1]:
            raise ValueError("HTML must be in (0, 1)")

        if monospace not in [0, 1]:
            raise ValueError("Monospace must be in (0, 1)")

        if html + monospace == 2:
            raise ValueError("HTML and Monospace are mutually exclusive")

        if attachment and attachment_base64:
            raise ValueError("Attachment and attachment_base64 are mutually exclusive")

        data = {
            "token": self.token,
            "user": user,
            "message": message
        }

        if title:
            data["title"] = title
        if device:
            data["device"] = device
        if html:
            data["html"] = html
        if monospace:
            data["monospace"] = monospace
        if priority != 0:
            data["priority"] = priority
        if sound:
            data["sound"] = sound
        if timestamp:
            data["timestamp"] = timestamp
        if ttl:
            data["ttl"] = ttl
        if url:
            data["url"] = url
        if url_title:
            data["url_title"] = url_title

        files = {}
        if attachment:
            files["attachment"] = open(attachment, "rb")

        if attachment_base64:
            data["attachment_base64"] = attachment_base64
            if attachment_type:
                data["attachment_type"] = attachment_type

        response = requests.post("https://api.pushover.net/1/messages.json", data=data, files=files)
        response.raise_for_status()
        return response.json()