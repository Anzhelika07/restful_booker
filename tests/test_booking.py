import pytest
from models.request_models import BookingRequest, BookingDates


class TestBooking:
    def test_create_booking(self, booking_api):
        booking_data = BookingRequest(
            firstname="Jim",
            lastname="Brown",
            totalprice=111,
            depositpaid=True,
            bookingdates=BookingDates(checkin="2018-01-01", checkout="2019-01-01"),
            additionalneeds="Breakfast"
        )

        response = booking_api.create_booking(booking_data)
        assert response.status_code == 200

        booking_response = response.json()
        assert booking_response["booking"]["firstname"] == booking_data.firstname
        assert booking_response["booking"]["lastname"] == booking_data.lastname

    def test_update_booking(self, booking_api, auth_token):
        # Create booking
        booking_data = BookingRequest(
            firstname="Alice",
            lastname="Smith",
            totalprice=200,
            depositpaid=True,
            bookingdates=BookingDates(checkin="2020-01-01", checkout="2020-01-02")
        )
        create_response = booking_api.create_booking(booking_data)
        booking_id = create_response.json()["bookingid"]

        # Update booking
        updated_data = BookingRequest(
            firstname="Bob",
            lastname="Johnson",
            totalprice=300,
            depositpaid=False,
            bookingdates=BookingDates(checkin="2021-01-01", checkout="2021-01-02")
        )
        update_response = booking_api.update_booking(booking_id, updated_data, auth_token)
        assert update_response.status_code == 200

        # Verify update
        get_response = booking_api.get_booking(booking_id)
        updated_booking = get_response.json()
        assert updated_booking["firstname"] == updated_data.firstname
        assert updated_booking["lastname"] == updated_data.lastname
