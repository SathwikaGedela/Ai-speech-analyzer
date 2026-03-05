#!/usr/bin/env python3
"""
Test script to debug signin network error
"""

import requests
import json
import time

def test_backend_connection():
    """Test if backend is accessible"""
    try:
        response = requests.get('http://127.0.0.1:5000/api/user', timeout=5)
        print(f"✅ Backend is accessible. Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend at http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Backend connection error: {e}")
        return False

def test_signin_endpoint():
    """Test signin endpoint with sample data"""
    try:
        # First create a test user
        signup_data = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "phone": "1234567890",
            "password": "password123",
            "confirmPassword": "password123"
        }
        
        print("Creating test user...")
        signup_response = requests.post(
            'http://127.0.0.1:5000/api/signup',
            json=signup_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if signup_response.status_code == 201:
            print("✅ Test user created successfully")
        elif signup_response.status_code == 400 and "already registered" in signup_response.text:
            print("ℹ️ Test user already exists")
        else:
            print(f"⚠️ Signup response: {signup_response.status_code} - {signup_response.text}")
        
        # Now test signin
        signin_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        print("Testing signin...")
        signin_response = requests.post(
            'http://127.0.0.1:5000/api/signin',
            json=signin_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Signin Status Code: {signin_response.status_code}")
        print(f"Signin Response: {signin_response.text}")
        
        if signin_response.status_code == 200:
            print("✅ Signin successful!")
            return True
        else:
            print(f"❌ Signin failed: {signin_response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - backend may not be running")
        return False
    except Exception as e:
        print(f"❌ Signin test error: {e}")
        return False

def main():
    print("🔍 Testing backend connection and signin...")
    print("=" * 50)
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    if test_backend_connection():
        test_signin_endpoint()
    else:
        print("❌ Backend is not accessible. Please check if it's running.")

if __name__ == "__main__":
    main()