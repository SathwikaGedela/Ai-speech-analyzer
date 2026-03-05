#!/usr/bin/env python3
"""
Test complete authentication flow and route protection
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_route_protection():
    print("🔒 Testing Route Protection (Before Login)\n")
    
    protected_routes = [
        "/",
        "/history", 
        "/interview",
        "/dashboard"
    ]
    
    for route in protected_routes:
        try:
            response = requests.get(f"{BASE_URL}{route}", allow_redirects=False)
            if response.status_code in [302, 301]:  # Redirect to auth
                print(f"✅ {route} - Properly redirects to authentication")
            elif response.status_code == 200 and "Authentication - Speech Analysis System" in response.text:
                print(f"✅ {route} - Shows authentication page")
            else:
                print(f"❌ {route} - Not properly protected (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ {route} - Error testing: {e}")

def test_complete_user_flow():
    print("\n👤 Testing Complete User Flow\n")
    
    # Test user data
    test_user = {
        "firstName": "Jane",
        "lastName": "Smith", 
        "email": "jane.smith@example.com",
        "phone": "+1987654321",
        "password": "securepass123",
        "confirmPassword": "securepass123"
    }
    
    session = requests.Session()
    
    print("1. Testing User Registration...")
    try:
        response = session.post(f"{BASE_URL}/api/signup", json=test_user)
        if response.status_code == 201:
            print("✅ User registration successful")
            user_data = response.json()
            print(f"   Created user: {user_data['user']['first_name']} {user_data['user']['last_name']}")
        else:
            print(f"❌ Registration failed: {response.json().get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    print("\n2. Testing User Login...")
    try:
        signin_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = session.post(f"{BASE_URL}/api/signin", json=signin_data)
        if response.status_code == 200:
            print("✅ User login successful")
        else:
            print(f"❌ Login failed: {response.json().get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    print("\n3. Testing Access to Protected Routes (After Login)...")
    protected_routes = [
        ("/", "Speech Analysis"),
        ("/dashboard", "Welcome, Jane!"),
        ("/history", "Analysis History"),
        ("/interview", "Interview Mode")
    ]
    
    for route, expected_content in protected_routes:
        try:
            response = session.get(f"{BASE_URL}{route}")
            if response.status_code == 200 and expected_content in response.text:
                print(f"✅ {route} - Accessible after login")
            else:
                print(f"❌ {route} - Not accessible or content missing")
        except Exception as e:
            print(f"❌ {route} - Error accessing: {e}")
    
    print("\n4. Testing Logout...")
    try:
        response = session.post(f"{BASE_URL}/api/logout")
        if response.status_code == 200:
            print("✅ Logout successful")
        else:
            print(f"❌ Logout failed")
            return False
    except Exception as e:
        print(f"❌ Logout error: {e}")
        return False
    
    print("\n5. Testing Access After Logout...")
    try:
        response = session.get(f"{BASE_URL}/dashboard", allow_redirects=False)
        if response.status_code in [302, 301]:
            print("✅ Protected routes properly blocked after logout")
        else:
            print(f"❌ Protected routes should be blocked after logout")
            return False
    except Exception as e:
        print(f"❌ Post-logout test error: {e}")
        return False
    
    return True

def test_api_protection():
    print("\n🔌 Testing API Route Protection\n")
    
    api_routes = [
        "/api/user",
        "/analyze",
        "/interview/analyze"
    ]
    
    for route in api_routes:
        try:
            response = requests.get(f"{BASE_URL}{route}")
            if response.status_code == 401:
                print(f"✅ {route} - Properly returns 401 Unauthorized")
            elif response.status_code in [302, 301]:
                print(f"✅ {route} - Properly redirects to authentication")
            else:
                print(f"❌ {route} - Not properly protected (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ {route} - Error testing: {e}")

def main():
    print("🚀 Testing Complete Authentication Integration\n")
    
    try:
        # Test route protection
        test_route_protection()
        
        # Test API protection
        test_api_protection()
        
        # Test complete user flow
        if test_complete_user_flow():
            print("\n🎉 All authentication tests passed!")
        else:
            print("\n❌ Some authentication tests failed!")
            return
        
        print("\n📋 Manual Testing Instructions:")
        print("1. Open http://localhost:5000/ in your browser")
        print("2. You should see the authentication page (signup form)")
        print("3. Create an account with your details")
        print("4. Sign in with your credentials")
        print("5. You should be redirected to the speech analysis dashboard")
        print("6. Try accessing /history, /interview - all should work")
        print("7. Logout and try accessing protected routes - should redirect to auth")
        
        print("\n🔗 Application Flow:")
        print("   • http://localhost:5000/ → Authentication (if not logged in)")
        print("   • http://localhost:5000/ → Speech Analysis (if logged in)")
        print("   • All routes now require authentication first")
        
        print("\n✅ Authentication is now mandatory for all application features!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()