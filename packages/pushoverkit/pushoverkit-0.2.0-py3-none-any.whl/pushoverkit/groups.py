import requests

class Groups:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.pushover.net/1/groups"

    def create(self, name: str):
        data = {
            "token": self.token,
            "name": name,
        }
        res = requests.post(f"{self.base_url}.json", data=data)
        res.raise_for_status()
        return res.json()

    def rename(self, group_key: str, name: str):
        data = {
            "token": self.token,
            "name": name,
        }
        res = requests.post(f"{self.base_url}/{group_key}/rename.json", data=data)
        res.raise_for_status()
        return res.json()

    def list_groups(self):
        res = requests.get(f"{self.base_url}.json", params={"token": self.token})
        res.raise_for_status()
        return res.json()

    def list_users(self, group_key: str):
        res = requests.get(f"{self.base_url}/{group_key}.json", params={"token": self.token})
        res.raise_for_status()
        return res.json()

    def add_user(self, group_key: str, user: str, device: str = None, memo: str = None):
        data = {
            "token": self.token,
            "user": user,
        }
        if device:
            data["device"] = device
        if memo:
            data["memo"] = memo
        res = requests.post(f"{self.base_url}/{group_key}/add_user.json", data=data)
        res.raise_for_status()
        return res.json()

    def remove_user(self, group_key: str, user: str, device: str = None):
        data = {
            "token": self.token,
            "user": user,
        }
        if device:
            data["device"] = device
        res = requests.post(f"{self.base_url}/{group_key}/remove_user.json", data=data)
        res.raise_for_status()
        return res.json()

    def disable_user(self, group_key: str, user: str, device: str = None):
        data = {
            "token": self.token,
            "user": user,
        }
        if device:
            data["device"] = device
        res = requests.post(f"{self.base_url}/{group_key}/disable_user.json", data=data)
        res.raise_for_status()
        return res.json()

    def enable_user(self, group_key: str, user: str, device: str = None):
        data = {
            "token": self.token,
            "user": user,
        }
        if device:
            data["device"] = device
        res = requests.post(f"{self.base_url}/{group_key}/enable_user.json", data=data)
        res.raise_for_status()
        return res.json()