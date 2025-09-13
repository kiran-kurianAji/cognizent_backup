#!/usr/bin/env python3
"""
Quick signup test
"""

import requests
import json

def test_signup():
    try:
        # Test data
        signup_data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
            "phone": "1234567890",
            "city": "Test City",
            "role": "client"
        }
        
        print("Testing signup...")
        print(f"Data: {json.dumps(signup_data, indent=2)}")
        
        response = requests.post(
            "http://localhost:8000/api/v1/auth/register",
            json=signup_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_signup()
