#!/usr/bin/env python3
"""
Test Signin with Detailed Error Information
"""

import requests
import json

def test_signin_detailed():
    """Test signin with detailed error reporting"""
    
    print("🔍 Testing Signin with Detailed Error Information...")
    
    base_url = "http://localhost:5000"
    
    # Test signin with detailed error handling
    try:
        headers = {
            'Content-Type': 'application/json',
            'Origin': 'http://localhost:5175'
        }
        
        # Test with invalid credentials
        test_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = requests.post(
            f"{base_url}/api/signin", 
            headers=headers,
            json=test_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response JSON: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
            
        # Test with missing data
        print("\n--- Testing with missing data ---")
        response2 = requests.post(
            f"{base_url}/api/signin", 
            headers=headers,
            json={},
            timeout=10
        )
        
        print(f"Status Code: {response2.status_code}")
        try:
            response_data2 = response2.json()
            print(f"Response JSON: {json.dumps(response_data2, indent=2)}")
        except:
            print(f"Response Text: {response2.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_signin_detailed()