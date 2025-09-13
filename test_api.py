#!/usr/bin/env python3
"""
Automated API Testing Script for Hotel Booking System
Run this to test all endpoints automatically
"""

import requests
import json
from datetime import date, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.client_token = None
        self.admin_token = None
        self.room_id = None
        self.booking_id = None
        
    def test_health_check(self):
        """Test health endpoint"""
        print("🔍 Testing Health Check...")
        response = self.session.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health check passed")
        
    def test_hotel_registration(self):
        """Test hotel registration"""
        print("🏨 Testing Hotel Registration...")
        hotel_data = {
            "hotel_name": "Test Grand Hotel",
            "contact_person": "Test Manager",
            "email": "test@testhotel.com",
            "password": "test123",
            "phone": "+1234567890",
            "city": "Test City",
            "address": "123 Test Street",
            "website": "https://testhotel.com",
            "description": "Test hotel for automated testing"
        }
        
        response = self.session.post(f"{API_BASE}/auth/hotel-register", json=hotel_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        self.admin_credentials = data["admin_credentials"]
        print(f"✅ Hotel registered: {data['data']['hotel_name']}")
        print(f"   Admin ID: {self.admin_credentials['user_id']}")
        
    def test_client_registration(self):
        """Test client registration"""
        print("👤 Testing Client Registration...")
        client_data = {
            "user_id": "C001",
            "email": "client@test.com",
            "password": "client123",
            "full_name": "Test Client",
            "phone": "+1234567890",
            "city": "Test City",
            "role": "client"
        }
        
        response = self.session.post(f"{API_BASE}/auth/register", json=client_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        print("✅ Client registered")
        
    def test_admin_login(self):
        """Test admin login"""
        print("🔐 Testing Admin Login...")
        login_data = {
            "user_id": self.admin_credentials["user_id"],
            "password": self.admin_credentials["password"]
        }
        
        response = self.session.post(f"{API_BASE}/auth/admin-login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        self.admin_token = data["access_token"]
        print("✅ Admin login successful")
        
    def test_client_login(self):
        """Test client login"""
        print("🔐 Testing Client Login...")
        login_data = {
            "email": "client@test.com",
            "password": "client123"
        }
        
        response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        self.client_token = data["access_token"]
        print("✅ Client login successful")
        
    def test_room_creation(self):
        """Test room creation (admin)"""
        print("🏠 Testing Room Creation...")
        room_data = {
            "room_type": "Deluxe Suite",
            "room_code": "room_type_1",
            "total_rooms": 10,
            "available_rooms": 10,
            "price": 299.99
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.session.post(f"{API_BASE}/rooms/", json=room_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        self.room_id = data["room_id"]
        print(f"✅ Room created: {data['room_type']} (ID: {self.room_id})")
        
    def test_booking_creation(self):
        """Test booking creation (client)"""
        print("📅 Testing Booking Creation...")
        booking_data = {
            "room_id": self.room_id,
            "arrival_date": (date.today() + timedelta(days=30)).isoformat(),
            "no_of_adults": 2,
            "no_of_children": 0,
            "no_of_week_nights": 3,
            "no_of_weekend_nights": 2,
            "type_of_meal_plan": 1,
            "no_of_special_requests": 0
        }
        
        headers = {"Authorization": f"Bearer {self.client_token}"}
        response = self.session.post(f"{API_BASE}/bookings/", json=booking_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        self.booking_id = data["booking_id"]
        print(f"✅ Booking created (ID: {self.booking_id})")
        print(f"   Lead time: {data['lead_time']} days")
        print(f"   Room type: {data['room_type_reserved']}")
        print(f"   Repeated guest: {data['repeated_guest']}")
        
    def test_ml_prediction(self):
        """Test ML prediction endpoint"""
        print("🤖 Testing ML Prediction...")
        prediction_data = {
            "booking_id": self.booking_id
        }
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.session.post(f"{API_BASE}/bookings/predict-cancellation", json=prediction_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        print(f"✅ ML Prediction: {data['cancellation_prediction']}")
        
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Automated API Tests...\n")
        
        try:
            self.test_health_check()
            self.test_hotel_registration()
            self.test_client_registration()
            self.test_admin_login()
            self.test_client_login()
            self.test_room_creation()
            self.test_booking_creation()
            self.test_ml_prediction()
            
            print("\n🎉 All tests passed successfully!")
            print("✅ Hotel Booking System is working perfectly!")
            
        except Exception as e:
            print(f"\n❌ Test failed: {str(e)}")
            raise

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
