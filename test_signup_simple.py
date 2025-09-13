import requests
import json

# Test signup
data = {
    "full_name": "Test User",
    "email": "testuser123@example.com", 
    "password": "testpass123",
    "phone": "1234567890",
    "city": "Test City",
    "role": "client"
}

try:
    response = requests.post(
        "http://localhost:8000/api/v1/auth/register",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
