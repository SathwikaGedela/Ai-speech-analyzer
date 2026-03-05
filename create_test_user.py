#!/usr/bin/env python3
"""
Create Test User via API
"""

import requests
import json

def create_test_user():
    """Create a test user via the API"""
    
    print("🔧 Creating Test User...")
    
    base_url = "http://localhost:5000"
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Origin': 'http://localhost:5175'
        }
        
        response = requests.post(
            f"{base_url}/api/create-test-user", 
            headers=headers,
            json={},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
            
        if response.status_code in [200, 201]:
            print("✅ Test user created/exists successfully")
            
            # Now test signin with the test user
            print("\n🧪 Testing signin with test user...")
            signin_data = {
                'email': 'test@example.com',
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
                print("✅ Signin working successfully!")
            else:
                print("❌ Signin still failing")
        else:
            print("❌ Failed to create test user")
            
    except Exception as e:
        print(f"Request failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_user()