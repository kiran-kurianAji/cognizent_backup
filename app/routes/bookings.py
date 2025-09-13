"""
Booking management routes for the Hotel Booking Cancellation Prediction System.
Handles booking creation, retrieval, updates, and cancellation prediction.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models import (
    BookingCreate, 
    BookingResponse, 
    BookingUpdate, 
    APIResponse, 
    PaginatedResponse,
    PredictionRequest,
    PredictionResponse
)
from app.auth import get_current_client, get_current_admin, get_current_user, TokenData
from app.database import get_db_client

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    current_user: TokenData = Depends(get_current_client)
):
    """
    Create a new booking (Client only).
    
    Args:
        booking_data: Booking creation data
        current_user: Current client user
        
    Returns:
        BookingResponse: Created booking details
    """
    try:
        client = get_db_client()
        
        # Check if room exists and is available
        room_result = client.table("rooms").select("*").eq("room_id", booking_data.room_id).execute()
        
        if not room_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        
        room = room_result.data[0]
        
        if room["available_rooms"] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room is not available"
            )
        
        # Calculate ML features automatically
        from datetime import date
        
        # Calculate lead_time (days between booking and arrival)
        booking_date = date.today()
        lead_time = (booking_data.arrival_date - booking_date).days
        
        # Extract arrival month
        arrival_month = booking_data.arrival_date.month
        
        # Get user's cancellation history
        history_result = client.table("history").select("history_id").eq("user_id", current_user.user_id).execute()
        no_of_previous_cancellations = len(history_result.data) if history_result.data else 0
        
        # Check if user is repeated guest
        previous_bookings = client.table("bookings").select("booking_id").eq("user_id", current_user.user_id).execute()
        repeated_guest = len(previous_bookings.data) > 0 if previous_bookings.data else False
        
        # Get room details for ML features
        room_type_reserved = room["room_code"]  # Map to ML-compatible code
        avg_price_per_room = float(room["price"])
        
        # Determine market segment (could be based on booking channel)
        market_segment_type = "Online"  # Default for API bookings
        
        # Prepare booking data for database
        booking_db_data = {
            "user_id": current_user.user_id,
            "room_id": booking_data.room_id,
            "lead_time": lead_time,
            "market_segment_type": market_segment_type,
            "no_of_children": booking_data.no_of_children,
            "no_of_adults": booking_data.no_of_adults,
            "arrival_date": booking_data.arrival_date.isoformat(),
            "arrival_month": arrival_month,
            "no_of_previous_cancellations": no_of_previous_cancellations,
            "room_type_reserved": room_type_reserved,
            "no_of_week_nights": booking_data.no_of_week_nights,
            "no_of_weekend_nights": booking_data.no_of_weekend_nights,
            "repeated_guest": repeated_guest,
            "type_of_meal_plan": booking_data.type_of_meal_plan,
            "no_of_special_requests": booking_data.no_of_special_requests,
            "avg_price_per_room": avg_price_per_room,
            "status": "confirmed"
        }
        
        # Insert booking into database
        result = client.table("bookings").insert(booking_db_data).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create booking"
            )
        
        # Update room availability
        new_available = room["available_rooms"] - 1
        client.table("rooms").update({"available_rooms": new_available}).eq("room_id", booking_data.room_id).execute()
        
        booking = result.data[0]
        
        return BookingResponse(
            booking_id=booking["booking_id"],
            user_id=booking["user_id"],
            room_id=booking["room_id"],
            lead_time=booking["lead_time"],
            market_segment_type=booking["market_segment_type"],
            no_of_children=booking["no_of_children"],
            no_of_adults=booking["no_of_adults"],
            arrival_date=booking["arrival_date"],
            arrival_month=booking["arrival_month"],
            no_of_previous_cancellations=booking["no_of_previous_cancellations"],
            room_type_reserved=booking["room_type_reserved"],
            no_of_week_nights=booking["no_of_week_nights"],
            no_of_weekend_nights=booking["no_of_weekend_nights"],
            repeated_guest=booking["repeated_guest"],
            type_of_meal_plan=booking["type_of_meal_plan"],
            no_of_special_requests=booking["no_of_special_requests"],
            avg_price_per_room=booking["avg_price_per_room"],
            booking_time=booking["booking_time"],
            cancellation_prediction=booking.get("cancellation_prediction"),
            status=booking["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create booking: {str(e)}"
        )


@router.get("/", response_model=List[BookingResponse])
async def get_bookings(
    current_user: TokenData = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of bookings to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of bookings to return"),
    status_filter: Optional[str] = Query(None, description="Filter by booking status")
):
    """
    Get bookings for the current user.
    
    Args:
        current_user: Current authenticated user
        skip: Number of bookings to skip for pagination
        limit: Maximum number of bookings to return
        status_filter: Filter by booking status
        
    Returns:
        List[BookingResponse]: List of bookings
    """
    try:
        client = get_db_client()
        
        # Build query
        query = client.table("bookings").select("*").eq("user_id", current_user.user_id)
        
        # Apply status filter
        if status_filter:
            query = query.eq("status", status_filter)
        
        # Apply pagination
        query = query.range(skip, skip + limit - 1).order("booking_time", desc=True)
        
        # Execute query
        result = query.execute()
        
        if not result.data:
            return []
        
        # Convert to response models
        bookings = []
        for booking in result.data:
            bookings.append(BookingResponse(
                booking_id=booking["booking_id"],
                user_id=booking["user_id"],
                room_id=booking["room_id"],
                lead_time=booking["lead_time"],
                market_segment_type=booking["market_segment_type"],
                no_of_children=booking["no_of_children"],
                no_of_adults=booking["no_of_adults"],
                arrival_date=booking["arrival_date"],
                arrival_month=booking["arrival_month"],
                no_of_previous_cancellations=booking["no_of_previous_cancellations"],
                room_type_reserved=booking["room_type_reserved"],
                no_of_week_nights=booking["no_of_week_nights"],
                no_of_weekend_nights=booking["no_of_weekend_nights"],
                repeated_guest=booking["repeated_guest"],
                type_of_meal_plan=booking["type_of_meal_plan"],
                no_of_special_requests=booking["no_of_special_requests"],
                avg_price_per_room=booking["avg_price_per_room"],
                booking_time=booking["booking_time"],
                cancellation_prediction=booking.get("cancellation_prediction"),
                status=booking["status"]
            ))
        
        return bookings
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch bookings: {str(e)}"
        )


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Get specific booking by ID.
    
    Args:
        booking_id: Booking ID to fetch
        current_user: Current authenticated user
        
    Returns:
        BookingResponse: Booking details
    """
    try:
        client = get_db_client()
        
        result = client.table("bookings").select("*").eq("booking_id", booking_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        booking = result.data[0]
        
        # Check if user has access to this booking
        if booking["user_id"] != current_user.user_id and current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this booking"
            )
        
        return BookingResponse(
            booking_id=booking["booking_id"],
            user_id=booking["user_id"],
            room_id=booking["room_id"],
            lead_time=booking["lead_time"],
            market_segment_type=booking["market_segment_type"],
            no_of_children=booking["no_of_children"],
            no_of_adults=booking["no_of_adults"],
            arrival_date=booking["arrival_date"],
            arrival_month=booking["arrival_month"],
            no_of_previous_cancellations=booking["no_of_previous_cancellations"],
            room_type_reserved=booking["room_type_reserved"],
            no_of_week_nights=booking["no_of_week_nights"],
            no_of_weekend_nights=booking["no_of_weekend_nights"],
            repeated_guest=booking["repeated_guest"],
            type_of_meal_plan=booking["type_of_meal_plan"],
            no_of_special_requests=booking["no_of_special_requests"],
            avg_price_per_room=booking["avg_price_per_room"],
            booking_time=booking["booking_time"],
            cancellation_prediction=booking.get("cancellation_prediction"),
            status=booking["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch booking: {str(e)}"
        )


@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Update booking details.
    
    Args:
        booking_id: Booking ID to update
        booking_update: Updated booking data
        current_user: Current authenticated user
        
    Returns:
        BookingResponse: Updated booking details
    """
    try:
        client = get_db_client()
        
        # Check if booking exists
        existing_booking = client.table("bookings").select("*").eq("booking_id", booking_id).execute()
        
        if not existing_booking.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        booking = existing_booking.data[0]
        
        # Check if user has access to this booking
        if booking["user_id"] != current_user.user_id and current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to update this booking"
            )
        
        # Prepare update data
        update_data = {}
        if booking_update.status is not None:
            update_data["status"] = booking_update.status.value
        if booking_update.cancellation_prediction is not None:
            update_data["cancellation_prediction"] = float(booking_update.cancellation_prediction)
        
        # Update booking
        result = client.table("bookings").update(update_data).eq("booking_id", booking_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update booking"
            )
        
        updated_booking = result.data[0]
        
        return BookingResponse(
            booking_id=updated_booking["booking_id"],
            user_id=updated_booking["user_id"],
            room_id=updated_booking["room_id"],
            lead_time=updated_booking["lead_time"],
            market_segment_type=updated_booking["market_segment_type"],
            no_of_children=updated_booking["no_of_children"],
            no_of_adults=updated_booking["no_of_adults"],
            arrival_date=updated_booking["arrival_date"],
            arrival_month=updated_booking["arrival_month"],
            no_of_previous_cancellations=updated_booking["no_of_previous_cancellations"],
            room_type_reserved=updated_booking["room_type_reserved"],
            no_of_week_nights=updated_booking["no_of_week_nights"],
            no_of_weekend_nights=updated_booking["no_of_weekend_nights"],
            repeated_guest=updated_booking["repeated_guest"],
            type_of_meal_plan=updated_booking["type_of_meal_plan"],
            no_of_special_requests=updated_booking["no_of_special_requests"],
            avg_price_per_room=updated_booking["avg_price_per_room"],
            booking_time=updated_booking["booking_time"],
            cancellation_prediction=updated_booking.get("cancellation_prediction"),
            status=updated_booking["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update booking: {str(e)}"
        )


@router.post("/{booking_id}/cancel", response_model=APIResponse)
async def cancel_booking(
    booking_id: int,
    current_user: TokenData = Depends(get_current_client)
):
    """
    Cancel a booking (Client only).
    
    Args:
        booking_id: Booking ID to cancel
        current_user: Current client user
        
    Returns:
        APIResponse: Cancellation confirmation
    """
    try:
        client = get_db_client()
        
        # Check if booking exists and belongs to user
        booking_result = client.table("bookings").select("*").eq("booking_id", booking_id).eq("user_id", current_user.user_id).execute()
        
        if not booking_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found or access denied"
            )
        
        booking = booking_result.data[0]
        
        if booking["status"] == "canceled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking is already canceled"
            )
        
        # Update booking status to canceled
        client.table("bookings").update({"status": "canceled"}).eq("booking_id", booking_id).execute()
        
        # Add to cancellation history
        history_data = {
            "user_id": current_user.user_id,
            "booking_id": booking_id
        }
        client.table("history").insert(history_data).execute()
        
        # Update room availability
        room_result = client.table("rooms").select("available_rooms").eq("room_id", booking["room_id"]).execute()
        if room_result.data:
            current_available = room_result.data[0]["available_rooms"]
            client.table("rooms").update({"available_rooms": current_available + 1}).eq("room_id", booking["room_id"]).execute()
        
        return APIResponse(
            success=True,
            message="Booking canceled successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel booking: {str(e)}"
        )


# ML Prediction Endpoints (Placeholder for future ML integration)
@router.post("/predict-cancellation", response_model=PredictionResponse)
async def predict_cancellation(
    prediction_request: PredictionRequest,
    current_user: TokenData = Depends(get_current_admin)
):
    """
    Predict cancellation probability for a booking (Admin only).
    
    TODO: Integrate ML model here for cancellation prediction.
    This endpoint is prepared for ML model integration.
    
    Args:
        prediction_request: Booking ID for prediction
        current_user: Current admin user
        
    Returns:
        PredictionResponse: Cancellation prediction with confidence score
    """
    try:
        client = get_db_client()
        
        # Get booking details for ML prediction
        booking_result = client.table("bookings").select("*").eq("booking_id", prediction_request.booking_id).execute()
        
        if not booking_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        booking = booking_result.data[0]
        
        # TODO: Integrate ML model here
        # This is where you'll add your ML model code
        # Example structure:
        # 1. Extract features from booking data
        # 2. Preprocess features for ML model
        # 3. Run ML model prediction
        # 4. Return prediction results
        
        # Placeholder prediction (replace with actual ML model)
        import random
        from datetime import datetime
        
        # Mock prediction for demonstration
        mock_prediction = round(random.uniform(0.1, 0.9), 2)
        mock_confidence = round(random.uniform(0.7, 0.95), 2)
        
        # Update booking with prediction
        client.table("bookings").update({
            "cancellation_prediction": mock_prediction
        }).eq("booking_id", prediction_request.booking_id).execute()
        
        return PredictionResponse(
            booking_id=prediction_request.booking_id,
            cancellation_prediction=mock_prediction,
            confidence_score=mock_confidence,
            prediction_timestamp=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict cancellation: {str(e)}"
        )
