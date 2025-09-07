import requests
from models.request_models import BookingRequest
from utils.retry import make_request_with_retry, APIError

class BookingAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.booking_url = f"{base_url}/booking"

    def get_booking_ids(self):
        return make_request_with_retry(requests.get, self.booking_url)

    def get_booking(self, booking_id):
        return make_request_with_retry(requests.get, f"{self.booking_url}/{booking_id}")

    def create_booking(self, booking: BookingRequest):
        return make_request_with_retry(
            requests.post,
            self.booking_url,
            json=booking.dict()
        )

    def update_booking(self, booking_id, booking: BookingRequest, token):
        headers = {"Cookie": f"token={token}"}
        return make_request_with_retry(
            requests.put,
            f"{self.booking_url}/{booking_id}",
            json=booking.dict(),
            headers=headers
        )

    def partial_update_booking(self, booking_id, updates: dict, token):
        headers = {"Cookie": f"token={token}"}
        return make_request_with_retry(
            requests.patch,
            f"{self.booking_url}/{booking_id}",
            json=updates,
            headers=headers
        )

    def delete_booking(self, booking_id, token):
        headers = {"Cookie": f"token={token}"}
        return make_request_with_retry(
            requests.delete,
            f"{self.booking_url}/{booking_id}",
            headers=headers
        )