#!/usr/bin/env python3
"""
Test script for integrated authentication system
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_auth_system():
    print("🔐 Testing Integrated Authentication System\n")
    
    # Test data
    test_user = {
        "firstName": "John",
        "lastName": "Doe", 
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "password": "password123",
        "confirmPassword": "password123"
    }
    
    print("1. Testing Signup...")
    try:
        response = requests.post(f"{BASE_URL}/api/signup", json=test_user)
        if response.status_code == 201:
            print("✅ Signup successful")
            user_data = response.json()
            print(f"   Created user: {user_data['user']['first_name']} {user_data['user']['last_name']}")
        else:
            print(f"❌ Signup failed: {response.json().get('error', 'Unknown error')}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server. Make sure it's running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Signup error: {e}")
        return False
    
    print("\n2. Testing Signin...")
    try:
        signin_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(f"{BASE_URL}/api/signin", json=signin_data)
        if response.status_code == 200:
            print("✅ Signin successful")
            # Save cookies for session
            session_cookies = response.cookies
        else:
            print(f"❌ Signin failed: {response.json().get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Signin error: {e}")
        return False
    
    print("\n3. Testing Protected Route (Get Current User)...")
    try:
        response = requests.get(f"{BASE_URL}/api/user", cookies=session_cookies)
        if response.status_code == 200:
            print("✅ Protected route accessible")
            user_data = response.json()['user']
            print(f"   Current user: {user_data['first_name']} {user_data['last_name']}")
        else:
            print(f"❌ Protected route failed: {response.json().get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Protected route error: {e}")
        return False
    
    print("\n4. Testing Logout...")
    try:
        response = requests.post(f"{BASE_URL}/api/logout", cookies=session_cookies)
        if response.status_code == 200:
            print("✅ Logout successful")
        else:
            print(f"❌ Logout failed: {response.json().get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Logout error: {e}")
        return False
    
    print("\n5. Testing Access After Logout...")
    try:
        response = requests.get(f"{BASE_URL}/api/user", cookies=session_cookies)
        if response.status_code == 401:
            print("✅ Protected route properly blocked after logout")
        else:
            print(f"❌ Protected route should be blocked after logout")
            return False
    except Exception as e:
        print(f"❌ Post-logout test error: {e}")
        return False
    
    return True

def test_validation():
    print("\n🔍 Testing Form Validation\n")
    
    # Test invalid email
    print("1. Testing invalid email...")
    invalid_user = {
        "firstName": "Test",
        "lastName": "User",
        "email": "invalid-email",
        "phone": "+1234567890",
        "password": "password123",
        "confirmPassword": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/signup", json=invalid_user)
        if response.status_code == 400 and "valid email" in response.json().get('error', ''):
            print("✅ Invalid email properly rejected")
        else:
            print(f"❌ Invalid email validation failed")
    except Exception as e:
        print(f"❌ Email validation test error: {e}")
    
    # Test password mismatch
    print("\n2. Testing password mismatch...")
    mismatch_user = {
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "phone": "+1234567890",
        "password": "password123",
        "confirmPassword": "different123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/signup", json=mismatch_user)
        if response.status_code == 400 and "match" in response.json().get('error', ''):
            print("✅ Password mismatch properly rejected")
        else:
            print(f"❌ Password mismatch validation failed")
    except Exception as e:
        print(f"❌ Password validation test error: {e}")

def main():
    print("🚀 Testing Integrated Authentication System for Speech Analysis\n")
    
    # Test basic auth flow
    if test_auth_system():
        print("\n🎉 All authentication tests passed!")
    else:
        print("\n❌ Some authentication tests failed!")
        return
    
    # Test validation
    test_validation()
    
    print("\n📋 Manual Testing Instructions:")
    print("1. Open http://localhost:5000/auth in your browser")
    print("2. Fill out the signup form and create an account")
    print("3. Sign in with your credentials")
    print("4. View the dashboard with your user details")
    print("5. Click logout to return to auth page")
    print("6. Try accessing http://localhost:5000/dashboard directly (should redirect)")
    
    print("\n🔗 Available Routes:")
    print("   • http://localhost:5000/auth - Authentication page")
    print("   • http://localhost:5000/dashboard - User dashboard (requires login)")
    print("   • http://localhost:5000/ - Main speech analysis (existing)")
    print("   • http://localhost:5000/interview - Interview mode (existing)")
    print("   • http://localhost:5000/history - Analysis history (existing)")

if __name__ == "__main__":
    main()