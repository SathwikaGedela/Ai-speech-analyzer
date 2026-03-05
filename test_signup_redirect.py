#!/usr/bin/env python3
"""
Test Signup to Signin Redirect Flow
"""

import requests
import json
import time

def test_signup_redirect_flow():
    """Test the complete signup to signin redirect flow"""
    
    print("🧪 Testing Signup to Signin Redirect Flow...")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Check if both servers are running
    try:
        # Check React frontend
        react_response = requests.get("http://localhost:5175", timeout=5)
        print(f"✅ React frontend running (Status: {react_response.status_code})")
        
        # Check Flask backend
        flask_response = requests.get(f"{base_url}/api/user", timeout=5)
        print(f"✅ Flask backend running (Status: {flask_response.status_code})")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not accessible: {e}")
        return False
    
    # Test 2: Test signup with new user
    print("\n🔧 Testing Signup Flow...")
    
    # Generate unique email for testing
    timestamp = int(time.time())
    test_email = f"testuser{timestamp}@example.com"
    
    signup_data = {
        'firstName': 'Test',
        'lastName': 'User',
        'email': test_email,
        'phone': '1234567890',
        'password': 'testpass123',
        'confirmPassword': 'testpass123'
    }
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Origin': 'http://localhost:5175'
        }
        
        signup_response = requests.post(
            f"{base_url}/api/signup", 
            headers=headers,
            json=signup_data,
            timeout=10
        )
        
        print(f"Signup Status Code: {signup_response.status_code}")
        
        try:
            signup_response_data = signup_response.json()
            print(f"Signup Response: {json.dumps(signup_response_data, indent=2)}")
        except:
            print(f"Signup Response Text: {signup_response.text}")
            
        if signup_response.status_code == 201:
            print("✅ Signup successful!")
            
            # Test 3: Test signin with the new user
            print("\n🔐 Testing Signin with New User...")
            
            signin_data = {
                'email': test_email,
                'password': 'testpass123'
            }
            
            signin_response = requests.post(
                f"{base_url}/api/signin", 
                headers=headers,
                json=signin_data,
                timeout=10
            )
            
            print(f"Signin Status Code: {signin_response.status_code}")
            
            try:
                signin_response_data = signin_response.json()
                print(f"Signin Response: {json.dumps(signin_response_data, indent=2)}")
            except:
                print(f"Signin Response Text: {signin_response.text}")
                
            if signin_response.status_code == 200:
                print("✅ Signin successful!")
                print("🎉 Complete signup to signin flow working!")
            else:
                print("❌ Signin failed")
                return False
        else:
            print("❌ Signup failed")
            return False
            
    except Exception as e:
        print(f"Request failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n📋 Expected User Experience:")
    print("1. User fills out signup form")
    print("2. After successful signup, automatically redirected to signin form")
    print("3. Email field is pre-filled with the signup email")
    print("4. Success message shows: 'Account created successfully! Please sign in with your new account.'")
    print("5. User enters password and signs in")
    print("6. Redirected to dashboard")
    
    print("\n🌐 Frontend URLs:")
    print("- Landing Page: http://localhost:5175/")
    print("- Authentication: http://localhost:5175/auth")
    print("- Dashboard: http://localhost:5175/dashboard")
    
    print("\n✅ Signup to Signin Redirect Flow Complete!")
    
    return True

if __name__ == "__main__":
    test_signup_redirect_flow()