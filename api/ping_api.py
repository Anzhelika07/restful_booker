import requests

class PingAPI:
    def __init__(self, base_url):
        self.ping_url = f"{base_url}/ping"

    def health_check(self):
        return requests.get(self.ping_url)
    