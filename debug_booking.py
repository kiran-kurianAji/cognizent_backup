#!/usr/bin/env python3
"""
Simple debug script to test booking creation
"""

import httpx
import json
from datetime import date, timedelta

async def test_booking():
    """Test booking creation step by step."""
    
    print("🔍 Testing Booking Creation...")
    
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
        
        # Step 2: Register a test user
        print("\n2. Registering test user...")
        user_data = {
            "full_name": "Debug User",
            "email": "debug@test.com",
            "password": "testpass123",
            "phone": "1234567890",
            "city": "Test City",
            "role": "client"
        }
        
        try:
            response = await client.post("http://localhost:8000/api/v1/auth/register", json=user_data)
            print(f"   Registration: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                user_id = result["data"]["user_id"]
                token = result["access_token"]
                print(f"   ✅ User created: {user_id}")
            else:
                print(f"   ❌ Registration failed: {response.text}")
                return
        except Exception as e:
            print(f"   ❌ Registration error: {e}")
            return
        
        # Step 3: Login to get token
        print("\n3. Logging in...")
        login_data = {
            "user_id": user_id,
            "password": "testpass123"
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
        
        # Step 4: Check rooms
        print("\n4. Checking rooms...")
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = await client.get("http://localhost:8000/api/v1/rooms/", headers=headers)
            print(f"   Rooms API: {response.status_code}")
            if response.status_code == 200:
                rooms = response.json()
                print(f"   ✅ Found {len(rooms)} rooms")
                if rooms:
                    room_id = rooms[0]["room_id"]
                    print(f"   Using room ID: {room_id}")
                else:
                    print("   ❌ No rooms available")
                    return
            else:
                print(f"   ❌ Rooms API failed: {response.text}")
                return
        except Exception as e:
            print(f"   ❌ Rooms error: {e}")
            return
        
        # Step 5: Create booking
        print("\n5. Creating booking...")
        future_date = date.today() + timedelta(days=30)
        booking_data = {
            "room_id": room_id,
            "arrival_date": future_date.isoformat(),
            "no_of_adults": 2,
            "no_of_children": 1,
            "no_of_week_nights": 3,
            "no_of_weekend_nights": 2,
            "type_of_meal_plan": 1,
            "no_of_special_requests": 1
        }
        
        print(f"   Booking data: {json.dumps(booking_data, indent=2)}")
        
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
                print(f"   ✅ Booking created: {result.get('booking_id')}")
                print(f"   Lead time: {result.get('lead_time')}")
                print(f"   Repeated guest: {result.get('repeated_guest')}")
            else:
                print(f"   ❌ Booking failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Booking error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_booking())
