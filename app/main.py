"""
Main FastAPI application for the Hotel Booking Cancellation Prediction System.
Configures the application, middleware, and includes all API routes.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from app.config import settings
from app.database import db_manager
from app.routes import auth, rooms, bookings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    print("Starting Hotel Booking Cancellation Prediction System...")
    
    # Test database connection
    connection_ok = await db_manager.test_connection()
    if not connection_ok:
        print("Warning: Database connection test failed")
    else:
        print("Database connection successful")
    
    yield
    
    # Shutdown
    print("Shutting down Hotel Booking Cancellation Prediction System...")


# Create FastAPI application
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="A FastAPI backend for hotel booking cancellation prediction using ML",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions globally."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions globally."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "data": None
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify application status.
    
    Returns:
        dict: Application health status
    """
    try:
        # Test database connection
        db_status = await db_manager.test_connection()
        
        return {
            "status": "healthy" if db_status else "unhealthy",
            "database": "connected" if db_status else "disconnected",
            "version": settings.version,
            "environment": "development" if settings.debug else "production"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "version": settings.version,
            "error": str(e)
        }


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: API information and available endpoints
    """
    return {
        "message": "Welcome to Hotel Booking Cancellation Prediction System API",
        "version": settings.version,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "api_prefix": settings.api_v1_prefix
    }


# Include API routes
app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(rooms.router, prefix=settings.api_v1_prefix)
app.include_router(bookings.router, prefix=settings.api_v1_prefix)


# Development server configuration
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )
