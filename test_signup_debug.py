#!/usr/bin/env python3
"""
Debug signup endpoint
"""

import requests
import json

def test_signup():
    """Test signup endpoint directly."""
    
    print("🔍 Testing Signup Endpoint...")
    
    # Test data
    signup_data = {
        "full_name": "Test User Debug",
        "email": "testdebug@example.com",
        "password": "testpass123",
        "phone": "1234567890",
        "city": "Test City",
        "role": "client"
    }
    
    try:
        # Test health check first
        print("\n1. Testing health check...")
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"   Health: {health_response.status_code}")
        
        if health_response.status_code != 200:
            print("   ❌ Backend not responding")
            return
        
        # Test signup
        print("\n2. Testing signup...")
        print(f"   Signup data: {json.dumps(signup_data, indent=2)}")
        
        signup_response = requests.post(
            "http://localhost:8000/api/v1/auth/register",
            json=signup_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Signup status: {signup_response.status_code}")
        print(f"   Signup response: {signup_response.text}")
        
        if signup_response.status_code == 200:
            result = signup_response.json()
            print(f"   ✅ Signup successful!")
            print(f"   User ID: {result.get('data', {}).get('user_id')}")
            print(f"   Token: {result.get('access_token', '')[:20]}...")
        else:
            print(f"   ❌ Signup failed: {signup_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend. Is it running on port 8000?")
    except requests.exceptions.Timeout:
        print("   ❌ Request timed out")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_signup()
