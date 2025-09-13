"""
Authentication routes for user registration and login.
Handles both client and admin authentication.
"""

from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.models import UserCreate, UserResponse, UserLogin, AdminLogin, HotelRegistration, HotelRegistrationResponse, Token, APIResponse
from app.auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash, 
    generate_user_id,
    get_current_user,
    TokenData
)
from app.database import get_db_client
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/hotel-register", response_model=HotelRegistrationResponse)
async def register_hotel(hotel_data: HotelRegistration):
    """
    Register a new hotel (creates admin user with hotel info).
    
    Args:
        hotel_data: Hotel registration data
        
    Returns:
        HotelRegistrationResponse: Registration result with admin credentials
    """
    try:
        client = get_db_client()
        
        # Check if email already exists
        existing_user = client.table("users").select("*").eq("email", hotel_data.email).execute()
        if existing_user.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Generate hotel admin user ID (A + random string)
        import random
        import string
        admin_id = "A" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
        
        # Create hotel admin user (hotel = admin)
        admin_user_data = {
            "user_id": admin_id,
            "role": "admin",
            "email": hotel_data.email,
            "password_hash": get_password_hash(hotel_data.password),
            "full_name": hotel_data.contact_person,
            "phone": hotel_data.phone,
            "city": hotel_data.city,
            "hotel_name": hotel_data.hotel_name,
            "hotel_address": hotel_data.address,
            "hotel_website": hotel_data.website,
            "hotel_description": hotel_data.description,
            "hotel_phone": hotel_data.phone,
            "hotel_contact_person": hotel_data.contact_person
        }
        
        # Insert admin user
        result = client.table("users").insert(admin_user_data).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create admin user"
            )
        
        # Hotel information is stored in the admin user record (hotel = admin)
        
        return HotelRegistrationResponse(
            success=True,
            message="Hotel registered successfully",
            data={
                "hotel_name": hotel_data.hotel_name,
                "admin_user_id": admin_id,
                "contact_person": hotel_data.contact_person,
                "email": hotel_data.email,
                "city": hotel_data.city
            },
            admin_credentials={
                "user_id": admin_id,
                "password": hotel_data.password,
                "note": "Save these credentials for hotel admin login"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/register", response_model=APIResponse)
async def register_user(user_data: UserCreate):
    """
    Register a new user (client or admin).
    
    Args:
        user_data: User registration data including email, password, and role
        
    Returns:
        APIResponse: Success message with user details
    """
    try:
        client = get_db_client()
        
        # Check if user already exists
        existing_user = client.table("users").select("user_id").eq("email", user_data.email).execute()
        
        if existing_user.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Generate user ID
        user_id = generate_user_id(user_data.role)
        
        # Hash password
        password_hash = get_password_hash(user_data.password)
        
        # Prepare user data for database
        user_db_data = {
            "user_id": user_id,
            "role": user_data.role.value,
            "email": user_data.email,
            "password_hash": password_hash,
            "full_name": user_data.full_name,
            "phone": user_data.phone,
            "city": user_data.city
        }
        
        # Insert user into database
        result = client.table("users").insert(user_db_data).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        return APIResponse(
            success=True,
            message="User registered successfully",
            data={
                "user_id": user_id,
                "email": user_data.email,
                "role": user_data.role.value
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login_user(login_data: UserLogin):
    """
    Authenticate user and return JWT token.
    
    Args:
        login_data: User login credentials (email and password)
        
    Returns:
        Token: JWT access token with expiration
    """
    try:
        # Authenticate user
        user = await authenticate_user(login_data.email, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user["user_id"], "role": user["role"]},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/admin-login", response_model=Token)
async def login_admin(login_data: AdminLogin):
    """
    Authenticate admin user with user_id and password.
    
    Args:
        login_data: Admin login credentials (user_id and password)
        
    Returns:
        Token: JWT access token with expiration
    """
    try:
        client = get_db_client()
        
        # Find admin user by user_id
        result = client.table("users").select("*").eq("user_id", login_data.user_id).eq("role", "admin").execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin credentials"
            )
        
        user = result.data[0]
        
        # Verify password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        if not pwd_context.verify(login_data.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin credentials"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user["user_id"], "role": user["role"]},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Admin login failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: TokenData = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current authenticated user from JWT token
        
    Returns:
        UserResponse: Current user details
    """
    try:
        client = get_db_client()
        
        # Get user details from database
        result = client.table("users").select("*").eq("user_id", current_user.user_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user = result.data[0]
        
        return UserResponse(
            user_id=user["user_id"],
            role=user["role"],
            email=user["email"],
            full_name=user["full_name"],
            phone=user["phone"],
            city=user["city"],
            created_at=user["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user info: {str(e)}"
        )


@router.post("/logout", response_model=APIResponse)
async def logout_user(current_user: TokenData = Depends(get_current_user)):
    """
    Logout user (client-side token invalidation).
    
    Note: This is a placeholder for client-side token management.
    In a production system, you might want to implement token blacklisting.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        APIResponse: Logout confirmation
    """
    return APIResponse(
        success=True,
        message="Logged out successfully"
    )
