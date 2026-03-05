#!/usr/bin/env python3
"""
Test signin using localhost instead of 127.0.0.1
"""

import requests
import json

def test_localhost_signin():
    """Test signin using localhost"""
    try:
        signin_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        print("Testing signin via localhost...")
        response = requests.post(
            'http://localhost:5000/api/signin',
            json=signin_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Localhost signin successful!")
            return True
        else:
            print(f"❌ Localhost signin failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Localhost signin error: {e}")
        return False

if __name__ == "__main__":
    test_localhost_signin()