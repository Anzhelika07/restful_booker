import pytest
from api.booking_api import BookingAPI
from api.auth_api import AuthAPI
from api.ping_api import PingAPI
from utils.logger import setup_logging
from utils.data_generator import generate_booking_data, generate_auth_data

# Настройка логирования
setup_logging()

BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def booking_api():
    return BookingAPI(BASE_URL)


@pytest.fixture(scope="session")
def auth_api():
    return AuthAPI(BASE_URL)


@pytest.fixture(scope="session")
def ping_api():
    return PingAPI(BASE_URL)


@pytest.fixture
def auth_token(auth_api):
    auth_data = generate_auth_data()
    response = auth_api.create_token(auth_data)
    return response.json()["token"]


@pytest.fixture
def booking_data(request):
    # Используем имя теста для создания уникального суффикса
    test_name = request.node.name
    return generate_booking_data(unique_suffix=test_name)


@pytest.fixture
def created_booking(booking_api, booking_data, auth_token):
    response = booking_api.create_booking(booking_data)
    booking_id = response.json()["bookingid"]
    yield booking_id, booking_data

    # Cleanup - удаляем созданный booking после теста
    try:
        booking_api.delete_booking(booking_id, auth_token)
    except Exception as e:
        # Логируем ошибку, но не падаем, чтобы не скрыть настоящую ошибку теста
        print(f"Error during cleanup: {e}")

    @pytest.fixture(autouse=True)
    def reset_state():
        # Код для сброса состояния перед каждым тестом
        yield
        # Код для очистки после каждого теста
