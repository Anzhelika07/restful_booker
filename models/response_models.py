from pydantic import BaseModel
from typing import Optional

class BookingResponse(BaseModel):
    bookingid: int
    booking: dict

class AuthResponse(BaseModel):
    token: str