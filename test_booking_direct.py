#!/usr/bin/env python3
"""
Direct booking test to bypass connection issues
"""

import asyncio
import httpx
from datetime import date, timedelta

async def test_booking_direct():
    """Test booking creation directly."""
    
    print("🔍 Testing Booking Creation Directly...")
    
    # Test data
    future_date = date.today() + timedelta(days=30)
    booking_data = {
        "room_id": 1,
        "arrival_date": future_date.isoformat(),
        "no_of_adults": 2,
        "no_of_children": 1,
        "no_of_week_nights": 3,
        "no_of_weekend_nights": 2,
        "type_of_meal_plan": 1,
        "no_of_special_requests": 1
    }
    
    print(f"📅 Booking data: {booking_data}")
    
    async with httpx.AsyncClient() as client:
        try:
            # Test health check first
            print("\n1. Testing health check...")
            response = await client.get("http://localhost:8000/health")
            print(f"   Health: {response.status_code}")
            
            if response.status_code != 200:
                print("   ❌ Backend not responding")
                return
            
            # Test booking creation
            print("\n2. Testing booking creation...")
            response = await client.post(
                "http://localhost:8000/api/v1/bookings/", 
                json=booking_data
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Booking created: {result}")
            else:
                print(f"   ❌ Booking failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_booking_direct())
