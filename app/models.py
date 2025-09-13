"""
Pydantic models for the Hotel Booking Cancellation Prediction System.
Defines data validation schemas for API requests and responses.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    CLIENT = "client"
    ADMIN = "admin"


class BookingStatus(str, Enum):
    """Booking status enumeration."""
    CONFIRMED = "confirmed"
    CANCELED = "canceled"


# Hotel Registration Models
class HotelRegistration(BaseModel):
    """Hotel registration model."""
    hotel_name: str = Field(..., min_length=1, max_length=200)
    contact_person: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: str = Field(..., min_length=10, max_length=15)
    city: str = Field(..., min_length=1, max_length=100)
    address: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class HotelRegistrationResponse(BaseModel):
    """Hotel registration response model."""
    success: bool
    message: str
    data: dict
    admin_credentials: dict

# User Models
class UserBase(BaseModel):
    """Base user model with common fields."""
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=6, max_length=100)
    role: UserRole = Field(default=UserRole.CLIENT)


class UserResponse(UserBase):
    """User response model (excludes sensitive data)."""
    user_id: str
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    """Admin login model (user_id + password)."""
    user_id: str = Field(..., min_length=6, max_length=20)
    password: str = Field(..., min_length=6)


# Room Models
class RoomBase(BaseModel):
    """Base room model."""
    room_type: str = Field(..., min_length=1, max_length=100)
    room_code: str = Field(..., pattern=r'^room_type_[1-9][0-9]*$')
    total_rooms: int = Field(..., gt=0)
    available_rooms: int = Field(..., ge=0)
    price: Decimal = Field(..., gt=0)
    
    @validator('available_rooms')
    def validate_available_rooms(cls, v, values):
        if 'total_rooms' in values and v > values['total_rooms']:
            raise ValueError('available_rooms cannot exceed total_rooms')
        return v


class RoomCreate(RoomBase):
    """Room creation model."""
    pass


class RoomResponse(RoomBase):
    """Room response model."""
    room_id: int
    
    class Config:
        from_attributes = True


# Booking Models
class BookingCreate(BaseModel):
    """Booking creation model - what users input."""
    room_id: int = Field(..., gt=0, description="ID of the room to book")
    arrival_date: date = Field(..., description="Check-in date")
    no_of_adults: int = Field(..., gt=0, description="Number of adults")
    no_of_children: int = Field(..., ge=0, description="Number of children")
    no_of_week_nights: int = Field(..., ge=0, description="Number of weeknights")
    no_of_weekend_nights: int = Field(..., ge=0, description="Number of weekend nights")
    type_of_meal_plan: int = Field(..., ge=0, le=2, description="1 for Non-veg, 2 for Veg")
    no_of_special_requests: int = Field(..., ge=0, description="Number of special requests")

class BookingBase(BaseModel):
    """Base booking model with all fields for database storage."""
    room_id: int = Field(..., gt=0)
    lead_time: int = Field(..., ge=0)
    market_segment_type: str = Field(..., min_length=1, max_length=50)
    no_of_children: int = Field(..., ge=0)
    no_of_adults: int = Field(..., gt=0)
    arrival_date: date
    arrival_month: int = Field(..., ge=1, le=12)
    no_of_previous_cancellations: int = Field(..., ge=0)
    room_type_reserved: str = Field(..., min_length=1, max_length=100)
    no_of_week_nights: int = Field(..., ge=0)
    no_of_weekend_nights: int = Field(..., ge=0)
    repeated_guest: int = Field(..., ge=0, description="Number of previous bookings made by this user")
    type_of_meal_plan: int = Field(..., ge=0)
    no_of_special_requests: int = Field(..., ge=0)
    avg_price_per_room: Decimal = Field(..., gt=0)




class BookingUpdate(BaseModel):
    """Booking update model."""
    status: Optional[BookingStatus] = None
    cancellation_prediction: Optional[Decimal] = Field(None, ge=0, le=1)


class BookingResponse(BookingBase):
    """Booking response model."""
    booking_id: int
    user_id: str
    booking_time: datetime
    cancellation_prediction: Optional[Decimal] = None
    status: BookingStatus
    
    class Config:
        from_attributes = True


# History Models
class HistoryResponse(BaseModel):
    """Cancellation history response model."""
    history_id: int
    user_id: str
    booking_id: int
    cancellation_date: datetime
    
    class Config:
        from_attributes = True


# Authentication Models
class Token(BaseModel):
    """JWT token response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    data: Optional[dict] = None


class TokenData(BaseModel):
    """JWT token data model."""
    user_id: Optional[str] = None
    role: Optional[UserRole] = None


# ML Prediction Models (for future integration)
class PredictionRequest(BaseModel):
    """ML prediction request model."""
    booking_id: int
    # Additional ML features can be added here when integrating the model


class PredictionResponse(BaseModel):
    """ML prediction response model."""
    booking_id: int
    cancellation_prediction: Decimal = Field(..., ge=0, le=1)
    confidence_score: Optional[Decimal] = Field(None, ge=0, le=1)
    prediction_timestamp: datetime
    
    class Config:
        from_attributes = True


# API Response Models
class APIResponse(BaseModel):
    """Standard API response model."""
    success: bool
    message: str
    data: Optional[dict] = None


class PaginatedResponse(BaseModel):
    """Paginated response model."""
    items: List[dict]
    total: int
    page: int
    per_page: int
    pages: int
