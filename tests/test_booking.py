import allure
import pytest

from utils.data_generator import generate_booking_data


@allure.feature("Booking API")
class TestBooking:
    @allure.story("Create Booking")
    @pytest.mark.parametrize("additional_needs", ["Breakfast", "WiFi", "Parking", None])
    def test_create_booking_with_different_needs(self, booking_api, additional_needs):
        booking_data = generate_booking_data()
        if additional_needs:
            booking_data.additionalneeds = additional_needs

        response = booking_api.create_booking(booking_data)
        assert response.status_code == 200

        booking_response = response.json()
        assert booking_response["booking"]["firstname"] == booking_data.firstname
        assert booking_response["booking"]["lastname"] == booking_data.lastname
        if additional_needs:
            assert booking_response["booking"]["additionalneeds"] == additional_needs

    @allure.story("Update Booking")
    def test_update_booking(self, booking_api, auth_token, created_booking):
        booking_id, original_data = created_booking

        # Обновляем данные
        updated_data = generate_booking_data()
        response = booking_api.update_booking(booking_id, updated_data, auth_token)
        assert response.status_code == 200

        # Проверяем обновление
        get_response = booking_api.get_booking(booking_id)
        updated_booking = get_response.json()
        assert updated_booking["firstname"] == updated_data.firstname
        assert updated_booking["lastname"] == updated_data.lastname

    @allure.story("Partial Update Booking")
    @pytest.mark.parametrize("field,value", [
        ("firstname", "UpdatedFirstName"),
        ("lastname", "UpdatedLastName"),
        ("totalprice", 999),
        ("additionalneeds", "UpdatedNeeds")
    ])
    def test_partial_update_booking(self, booking_api, auth_token, created_booking, field, value):
        booking_id, _ = created_booking

        # Частичное обновление
        updates = {field: value}
        response = booking_api.partial_update_booking(booking_id, updates, auth_token)
        assert response.status_code == 200

        # Проверяем обновление
        get_response = booking_api.get_booking(booking_id)
        updated_booking = get_response.json()
        assert updated_booking[field] == value

    @allure.story("Delete Booking")
    def test_delete_booking(self, booking_api, auth_token):
        # Создаем booking для удаления
        from utils.data_generator import generate_booking_data
        from utils.retry import APIError
        import pytest

        booking_data = generate_booking_data()
        create_response = booking_api.create_booking(booking_data)
        booking_id = create_response.json()["bookingid"]

        # Удаляем booking
        response = booking_api.delete_booking(booking_id, auth_token)
        assert response.status_code == 201

        # Проверяем, что booking удален - должен вернуть 404
        # Ожидаем исключение APIError с статусом 404
        with pytest.raises(APIError) as exc_info:
            booking_api.get_booking(booking_id)

        assert exc_info.value.status_code == 404
