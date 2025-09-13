"""
Authentication and authorization system for the Hotel Booking Cancellation Prediction System.
Handles JWT token generation, validation, and role-based access control.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from app.models import TokenData, UserRole
from app.database import get_db_client

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify and decode JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        
        if user_id is None or role is None:
            raise credentials_exception
        
        token_data = TokenData(user_id=user_id, role=UserRole(role))
        return token_data
    except JWTError:
        raise credentials_exception


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    return verify_token(token)


async def get_current_client(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """Ensure current user is a client."""
    if current_user.role != UserRole.CLIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Client access required."
        )
    return current_user


async def get_current_admin(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """Ensure current user is an admin."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin access required."
        )
    return current_user


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticate user with email and password."""
    try:
        client = get_db_client()
        
        # Query user by email
        result = client.table("users").select("*").eq("email", email).execute()
        
        if not result.data:
            return None
        
        user = result.data[0]
        
        # Verify password
        if not verify_password(password, user["password_hash"]):
            return None
        
        return user
    except Exception as e:
        print(f"Authentication error: {e}")
        return None


def generate_user_id(role: UserRole) -> str:
    """Generate a unique user ID based on role."""
    import uuid
    prefix = "C" if role == UserRole.CLIENT else "A"
    unique_id = str(uuid.uuid4()).replace("-", "")[:8]
    return f"{prefix}{unique_id}"


# Role-based access control decorators
def require_role(required_role: UserRole):
    """Decorator factory for role-based access control."""
    def role_checker(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. {required_role.value.title()} access required."
            )
        return current_user
    return role_checker
