"""
Room management routes for the Hotel Booking Cancellation Prediction System.
Handles room listing, creation, and updates.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models import RoomCreate, RoomResponse, APIResponse, PaginatedResponse
from app.auth import get_current_admin, get_current_user, TokenData
from app.database import get_db_client

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=List[RoomResponse])
async def get_rooms(
    skip: int = Query(0, ge=0, description="Number of rooms to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of rooms to return"),
    room_type: Optional[str] = Query(None, description="Filter by room type"),
    available_only: bool = Query(False, description="Show only available rooms")
):
    """
    Get list of rooms with optional filtering.
    
    Args:
        skip: Number of rooms to skip for pagination
        limit: Maximum number of rooms to return
        room_type: Filter by specific room type
        available_only: Show only rooms with availability
        
    Returns:
        List[RoomResponse]: List of rooms
    """
    try:
        client = get_db_client()
        
        # Build query
        query = client.table("rooms").select("*")
        
        # Apply filters
        if room_type:
            query = query.eq("room_type", room_type)
        
        if available_only:
            query = query.gt("available_rooms", 0)
        
        # Apply pagination
        query = query.range(skip, skip + limit - 1)
        
        # Execute query
        result = query.execute()
        
        if not result.data:
            return []
        
        # Convert to response models
        rooms = []
        for room in result.data:
            rooms.append(RoomResponse(
                room_id=room["room_id"],
                room_type=room["room_type"],
                room_code=room["room_code"],
                total_rooms=room["total_rooms"],
                available_rooms=room["available_rooms"],
                price=room["price"]
            ))
        
        return rooms
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch rooms: {str(e)}"
        )


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: int):
    """
    Get specific room by ID.
    
    Args:
        room_id: Room ID to fetch
        
    Returns:
        RoomResponse: Room details
    """
    try:
        client = get_db_client()
        
        result = client.table("rooms").select("*").eq("room_id", room_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        
        room = result.data[0]
        
        return RoomResponse(
            room_id=room["room_id"],
            room_type=room["room_type"],
            room_code=room["room_code"],
            total_rooms=room["total_rooms"],
            available_rooms=room["available_rooms"],
            price=room["price"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch room: {str(e)}"
        )


@router.post("/", response_model=RoomResponse)
async def create_room(
    room_data: RoomCreate,
    current_user: TokenData = Depends(get_current_admin)
):
    """
    Create a new room (Admin only).
    
    Args:
        room_data: Room creation data
        current_user: Current admin user
        
    Returns:
        RoomResponse: Created room details
    """
    try:
        client = get_db_client()
        
        # Check if room_code already exists
        existing_room = client.table("rooms").select("room_id").eq("room_code", room_data.room_code).execute()
        
        if existing_room.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room with this code already exists"
            )
        
        # Prepare room data for database
        room_db_data = {
            "room_type": room_data.room_type,
            "room_code": room_data.room_code,
            "total_rooms": room_data.total_rooms,
            "available_rooms": room_data.available_rooms,
            "price": float(room_data.price)
        }
        
        # Insert room into database
        result = client.table("rooms").insert(room_db_data).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create room"
            )
        
        room = result.data[0]
        
        return RoomResponse(
            room_id=room["room_id"],
            room_type=room["room_type"],
            room_code=room["room_code"],
            total_rooms=room["total_rooms"],
            available_rooms=room["available_rooms"],
            price=room["price"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create room: {str(e)}"
        )


@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: int,
    room_data: RoomCreate,
    current_user: TokenData = Depends(get_current_admin)
):
    """
    Update room details (Admin only).
    
    Args:
        room_id: Room ID to update
        room_data: Updated room data
        current_user: Current admin user
        
    Returns:
        RoomResponse: Updated room details
    """
    try:
        client = get_db_client()
        
        # Check if room exists
        existing_room = client.table("rooms").select("*").eq("room_id", room_id).execute()
        
        if not existing_room.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        
        # Check if room_code is being changed and if it conflicts
        if room_data.room_code != existing_room.data[0]["room_code"]:
            code_check = client.table("rooms").select("room_id").eq("room_code", room_data.room_code).execute()
            if code_check.data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Room with this code already exists"
                )
        
        # Prepare update data
        update_data = {
            "room_type": room_data.room_type,
            "room_code": room_data.room_code,
            "total_rooms": room_data.total_rooms,
            "available_rooms": room_data.available_rooms,
            "price": float(room_data.price)
        }
        
        # Update room
        result = client.table("rooms").update(update_data).eq("room_id", room_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update room"
            )
        
        room = result.data[0]
        
        return RoomResponse(
            room_id=room["room_id"],
            room_type=room["room_type"],
            room_code=room["room_code"],
            total_rooms=room["total_rooms"],
            available_rooms=room["available_rooms"],
            price=room["price"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update room: {str(e)}"
        )


@router.delete("/{room_id}", response_model=APIResponse)
async def delete_room(
    room_id: int,
    current_user: TokenData = Depends(get_current_admin)
):
    """
    Delete a room (Admin only).
    
    Args:
        room_id: Room ID to delete
        current_user: Current admin user
        
    Returns:
        APIResponse: Deletion confirmation
    """
    try:
        client = get_db_client()
        
        # Check if room exists
        existing_room = client.table("rooms").select("room_id").eq("room_id", room_id).execute()
        
        if not existing_room.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        
        # Check if room has active bookings
        active_bookings = client.table("bookings").select("booking_id").eq("room_id", room_id).eq("status", "confirmed").execute()
        
        if active_bookings.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete room with active bookings"
            )
        
        # Delete room
        result = client.table("rooms").delete().eq("room_id", room_id).execute()
        
        return APIResponse(
            success=True,
            message="Room deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete room: {str(e)}"
        )
