import pytest
from api.booking_api import BookingAPI
from api.auth_api import AuthAPI
from api.ping_api import PingAPI

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture
def booking_api():
    return BookingAPI(BASE_URL)

@pytest.fixture
def auth_api():
    return AuthAPI(BASE_URL)

@pytest.fixture
def ping_api():
    return PingAPI(BASE_URL)


@pytest.fixture
def auth_token(auth_api):
    from models.request_models import AuthRequest  # Добавляем импорт здесь

    auth_data = AuthRequest(username="admin", password="password123")
    response = auth_api.create_token(auth_data)
    return response.json()["token"]
