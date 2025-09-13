#!/usr/bin/env python3
"""
Quick API test - just test the main functionality
"""

import requests
import json

def quick_test():
    """Quick test of main endpoints"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Health...")
    health = requests.get(f"{base_url}/health")
    print(f"Health: {health.status_code} - {health.json()}")
    
    print("\n🏨 Testing Hotel Registration...")
    hotel_data = {
        "hotel_name": "Quick Test Hotel",
        "contact_person": "Test Manager",
        "email": "quick@test.com",
        "password": "test123",
        "phone": "+1234567890",
        "city": "Test City"
    }
    
    hotel_resp = requests.post(f"{base_url}/api/v1/auth/hotel-register", json=hotel_data)
    print(f"Hotel Registration: {hotel_resp.status_code}")
    
    if hotel_resp.status_code == 200:
        admin_creds = hotel_resp.json()["admin_credentials"]
        print(f"Admin ID: {admin_creds['user_id']}")
        
        print("\n🔐 Testing Admin Login...")
        login_data = {
            "user_id": admin_creds["user_id"],
            "password": admin_creds["password"]
        }
        
        login_resp = requests.post(f"{base_url}/api/v1/auth/admin-login", json=login_data)
        print(f"Admin Login: {login_resp.status_code}")
        
        if login_resp.status_code == 200:
            token = login_resp.json()["access_token"]
            print("✅ All quick tests passed!")
        else:
            print("❌ Admin login failed")
    else:
        print("❌ Hotel registration failed")

if __name__ == "__main__":
    quick_test()
