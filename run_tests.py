#!/usr/bin/env python3
"""
Simple test runner for Hotel Booking API
"""

import subprocess
import sys
import time

def run_api_tests():
    """Run the automated API tests"""
    print("🧪 Running Hotel Booking API Tests...")
    
    try:
        # Run the test script
        result = subprocess.run([sys.executable, "test_api.py"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            print(result.stdout)
        else:
            print("❌ Tests failed!")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ Tests timed out")
    except Exception as e:
        print(f"❌ Error running tests: {e}")

if __name__ == "__main__":
    run_api_tests()
