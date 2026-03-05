#!/usr/bin/env python3
"""
Test script to verify authentication endpoints are working after CORS fix
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_USER = {
    "firstName": "Test",
    "lastName": "User", 
    "email": "test@example.com",
    "phone": "+1234567890",
    "password": "testpass123",
    "confirmPassword": "testpass123"
}

def test_signup():
    """Test user signup endpoint"""
    print("🧪 Testing signup endpoint...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/signup",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Signup successful!")
            return True
        elif response.status_code == 400 and "Email already registered" in response.json().get('error', ''):
            print("ℹ️ User already exists, that's fine for testing")
            return True
        else:
            print("❌ Signup failed")
            return False
            
    except Exception as e:
        print(f"❌ Signup error: {e}")
        return False

def test_signin():
    """Test user signin endpoint"""
    print("\n🧪 Testing signin endpoint...")
    
    try:
        signin_data = {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        
        response = requests.post(
            f"{BASE_URL}/api/signin",
            json=signin_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Signin successful!")
            return True
        else:
            print("❌ Signin failed")
            return False
            
    except Exception as e:
        print(f"❌ Signin error: {e}")
        return False

def test_cors():
    """Test CORS preflight request"""
    print("\n🧪 Testing CORS preflight...")
    
    try:
        response = requests.options(
            f"{BASE_URL}/api/signin",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ CORS preflight successful!")
            return True
        else:
            print("❌ CORS preflight failed")
            return False
            
    except Exception as e:
        print(f"❌ CORS error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Authentication Endpoints After CORS Fix")
    print("=" * 50)
    
    # Test CORS first
    cors_ok = test_cors()
    
    # Test signup
    signup_ok = test_signup()
    
    # Test signin
    signin_ok = test_signin()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"CORS: {'✅' if cors_ok else '❌'}")
    print(f"Signup: {'✅' if signup_ok else '❌'}")
    print(f"Signin: {'✅' if signin_ok else '❌'}")
    
    if cors_ok and signup_ok and signin_ok:
        print("\n🎉 All tests passed! Authentication should work now.")
    else:
        print("\n⚠️ Some tests failed. Check the backend logs for details.")