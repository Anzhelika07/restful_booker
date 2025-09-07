from faker import Faker
from models.request_models import BookingRequest, BookingDates, AuthRequest

fake = Faker()

def generate_booking_data(unique_suffix=None):
    suffix = f"_{unique_suffix}" if unique_suffix else f"_{fake.random_int(1000, 9999)}"
    return BookingRequest(
        firstname=fake.first_name() + suffix,
        lastname=fake.last_name() + suffix,
        totalprice=fake.random_int(min=100, max=1000),
        depositpaid=fake.boolean(),
        bookingdates=BookingDates(
            checkin=fake.date_between(start_date='-1y', end_date='today').isoformat(),
            checkout=fake.date_between(start_date='today', end_date='+1y').isoformat()
        ),
        additionalneeds=fake.random_element(
            elements=("Breakfast", "Lunch", "Dinner", "WiFi", "Parking", "Swimming Pool")
        )
    )

def generate_auth_data():
    return AuthRequest(
        username="admin",
        password="password123"
    )
