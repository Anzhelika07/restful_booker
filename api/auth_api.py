import requests
from models.request_models import AuthRequest
from utils.retry import make_request_with_retry

class AuthAPI:
    def __init__(self, base_url):
        self.auth_url = f"{base_url}/auth"

    def create_token(self, auth_data: AuthRequest):
        return make_request_with_retry(
            requests.post,
            self.auth_url,
            json=auth_data.dict()
        )