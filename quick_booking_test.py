#!/usr/bin/env python3
"""
Quick test to debug booking creation
"""

import httpx
import json
from datetime import date, timedelta

async def test_booking():
    """Test booking creation with minimal data."""
    
    print("🔍 Quick Booking Test...")
    
    async with httpx.AsyncClient() as client:
        
        # Step 1: Test health check
        print("\n1. Testing health check...")
        try:
            response = await client.get("http://localhost:8000/health")
            print(f"   Health check: {response.status_code}")
            if response.status_code != 200:
                print("   ❌ Backend not responding")
                return
        except Exception as e:
            print(f"   ❌ Backend connection failed: {e}")
            return
        
        # Step 2: Login with existing user (from your screenshot: C5592a3ce)
        print("\n2. Testing login...")
        login_data = {
            "user_id": "C5592a3ce",  # From your screenshot
            "password": "testpass123"  # You'll need to use the actual password
        }
        
        try:
            response = await client.post("http://localhost:8000/api/v1/auth/login", json=login_data)
            print(f"   Login: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                token = result["access_token"]
                print(f"   ✅ Login successful")
            else:
                print(f"   ❌ Login failed: {response.text}")
                return
        except Exception as e:
            print(f"   ❌ Login error: {e}")
            return
        
        # Step 3: Test booking creation
        print("\n3. Testing booking creation...")
        future_date = date.today() + timedelta(days=30)
        booking_data = {
            "room_id": 1,
            "arrival_date": future_date.isoformat(),
            "no_of_adults": 2,
            "no_of_children": 0,
            "no_of_week_nights": 3,
            "no_of_weekend_nights": 2,
            "type_of_meal_plan": 1,
            "no_of_special_requests": 0
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = await client.post(
                "http://localhost:8000/api/v1/bookings/", 
                json=booking_data, 
                headers=headers
            )
            print(f"   Booking API: {response.status_code}")
            print(f"   Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Booking created successfully!")
            else:
                print(f"   ❌ Booking failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Booking error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_booking())
