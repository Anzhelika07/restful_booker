import requests
from models.request_models import AuthRequest

class AuthAPI:
    def __init__(self, base_url):
        self.auth_url = f"{base_url}/auth"

    def create_token(self, auth_data: AuthRequest):
        return requests.post(self.auth_url, json=auth_data.dict())
