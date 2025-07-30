import requests

class Teams:
    def __init__(self, team_token: str=None):
        self.team_token = team_token
        self.base_url = "https://api.pushover.net/1/teams"

    def add_user(self, email:str, team_token: str=None, name :str=None, password: str=None, instant: bool=False, admin: bool=False, group :str=None):
        if not team_token and not self.team_token:
            raise ValueError("You must specify a team_token")

        data = {
            "token": team_token or self.team_token,
            "email": email,
        }
        if name:
            data["name"] = name
        if password:
            data["password"] = password
        if instant:
            data["instant"] = "true"
        if admin:
            data["admin"] = "true"
        if group:
            data["group"] = group
        res = requests.post(f"{self.base_url}/add_user.json", data=data)
        res.raise_for_status()
        return res.json()


    def remove_user(self, email: str, team_token: str=None):
        if not team_token and not self.team_token:
            raise ValueError("You must specify a team_token")

        data = {
            "token": team_token or self.team_token,
            "email": email,
        }
        res = requests.post(f"{self.base_url}/remove_user.json", data=data)
        res.raise_for_status()
        return res.json()