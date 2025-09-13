#!/usr/bin/env python3
"""
Test script to verify frontend authentication flow
"""

import asyncio
import httpx
import json

async def test_auth_flow():
    """Test the complete authentication flow."""
    
    print("🔍 Testing Frontend Authentication Flow...")
    
    async with httpx.AsyncClient() as client:
        try:
            # Step 1: Test health check
            print("\n1. Testing health check...")
            response = await client.get("http://localhost:8000/health")
            print(f"   Health: {response.status_code}")
            
            if response.status_code != 200:
                print("   ❌ Backend not responding")
                return
            
            # Step 2: Register a test user
            print("\n2. Registering test user...")
            user_data = {
                "full_name": "Test User Frontend",
                "email": "testfrontend@example.com",
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
                    print(f"   ✅ Token received: {token[:20]}...")
                else:
                    print(f"   ❌ Registration failed: {response.text}")
                    return
            except Exception as e:
                print(f"   ❌ Registration error: {e}")
                return
            
            # Step 3: Test profile endpoint with token
            print("\n3. Testing profile endpoint...")
            headers = {"Authorization": f"Bearer {token}"}
            
            try:
                response = await client.get("http://localhost:8000/api/v1/auth/profile", headers=headers)
                print(f"   Profile API: {response.status_code}")
                if response.status_code == 200:
                    profile = response.json()
                    print(f"   ✅ Profile fetched: {profile.get('full_name')}")
                else:
                    print(f"   ❌ Profile failed: {response.text}")
            except Exception as e:
                print(f"   ❌ Profile error: {e}")
            
            # Step 4: Test rooms endpoint with token
            print("\n4. Testing rooms endpoint...")
            try:
                response = await client.get("http://localhost:8000/api/v1/rooms/", headers=headers)
                print(f"   Rooms API: {response.status_code}")
                if response.status_code == 200:
                    rooms = response.json()
                    print(f"   ✅ Rooms fetched: {len(rooms)} rooms")
                    if rooms:
                        print(f"   First room: {rooms[0]}")
                else:
                    print(f"   ❌ Rooms failed: {response.text}")
            except Exception as e:
                print(f"   ❌ Rooms error: {e}")
            
            # Step 5: Test bookings endpoint with token
            print("\n5. Testing bookings endpoint...")
            try:
                response = await client.get("http://localhost:8000/api/v1/bookings/", headers=headers)
                print(f"   Bookings API: {response.status_code}")
                if response.status_code == 200:
                    bookings = response.json()
                    print(f"   ✅ Bookings fetched: {len(bookings)} bookings")
                else:
                    print(f"   ❌ Bookings failed: {response.text}")
            except Exception as e:
                print(f"   ❌ Bookings error: {e}")
            
            print(f"\n✅ Authentication flow test completed!")
            print(f"   User ID: {user_id}")
            print(f"   Token: {token[:20]}...")
            print(f"\n📝 Frontend Instructions:")
            print(f"   1. Open browser console (F12)")
            print(f"   2. Run: localStorage.setItem('token', '{token}')")
            print(f"   3. Run: localStorage.setItem('userRole', 'client')")
            print(f"   4. Navigate to: http://localhost:8004/client-dashboard")
            print(f"   5. Try creating a booking")
                
        except Exception as e:
            print(f"   ❌ General error: {e}")

if __name__ == "__main__":
    asyncio.run(test_auth_flow())
