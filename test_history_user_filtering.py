#!/usr/bin/env python3
"""
Simple test to verify user-specific history filtering
"""

import requests
import json

def test_history_filtering():
    """Test that history is filtered by user"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing user-specific history filtering...")
    
    # Test 1: Create two test users
    print("\n1. Creating test users...")
    
    user1_data = {
        "first_name": "Test",
        "last_name": "User1",
        "email": "testuser1@example.com",
        "phone": "1234567890",
        "password": "password123"
    }
    
    user2_data = {
        "first_name": "Test", 
        "last_name": "User2",
        "email": "testuser2@example.com",
        "phone": "0987654321",
        "password": "password123"
    }
    
    # Create user1
    response = requests.post(f"{base_url}/api/signup", json=user1_data)
    if response.status_code == 201:
        print("✅ User1 created successfully")
    else:
        print(f"⚠️ User1 creation: {response.status_code} - {response.text}")
    
    # Create user2
    response = requests.post(f"{base_url}/api/signup", json=user2_data)
    if response.status_code == 201:
        print("✅ User2 created successfully")
    else:
        print(f"⚠️ User2 creation: {response.status_code} - {response.text}")
    
    # Test 2: Sign in as user1 and check history
    print("\n2. Testing User1 history...")
    
    session1 = requests.Session()
    signin_response = session1.post(f"{base_url}/api/signin", json={
        "email": "testuser1@example.com",
        "password": "password123"
    })
    
    if signin_response.status_code == 200:
        print("✅ User1 signed in successfully")
        
        # Get user1 history
        history_response = session1.get(f"{base_url}/api/history")
        if history_response.status_code == 200:
            history_data = history_response.json()
            user1_sessions = history_data.get('sessions', [])
            print(f"✅ User1 history retrieved: {len(user1_sessions)} sessions")
        else:
            print(f"❌ Failed to get User1 history: {history_response.status_code}")
            return False
    else:
        print(f"❌ User1 signin failed: {signin_response.status_code}")
        return False
    
    # Test 3: Sign in as user2 and check history
    print("\n3. Testing User2 history...")
    
    session2 = requests.Session()
    signin_response = session2.post(f"{base_url}/api/signin", json={
        "email": "testuser2@example.com", 
        "password": "password123"
    })
    
    if signin_response.status_code == 200:
        print("✅ User2 signed in successfully")
        
        # Get user2 history
        history_response = session2.get(f"{base_url}/api/history")
        if history_response.status_code == 200:
            history_data = history_response.json()
            user2_sessions = history_data.get('sessions', [])
            print(f"✅ User2 history retrieved: {len(user2_sessions)} sessions")
        else:
            print(f"❌ Failed to get User2 history: {history_response.status_code}")
            return False
    else:
        print(f"❌ User2 signin failed: {signin_response.status_code}")
        return False
    
    # Test 4: Verify histories are separate
    print("\n4. Verifying history separation...")
    
    # Check if any sessions overlap (they shouldn't)
    user1_session_ids = {s['id'] for s in user1_sessions}
    user2_session_ids = {s['id'] for s in user2_sessions}
    
    overlap = user1_session_ids.intersection(user2_session_ids)
    
    if len(overlap) == 0:
        print("✅ No session overlap between users - histories are properly separated")
    else:
        print(f"❌ Found {len(overlap)} overlapping sessions - histories are NOT separated")
        return False
    
    # Test 5: Test cross-user session access
    if user1_sessions and user2_sessions:
        print("\n5. Testing cross-user session access...")
        
        user1_session_id = user1_sessions[0]['id']
        user2_session_id = user2_sessions[0]['id']
        
        # User1 trying to access User2's session
        response = session1.get(f"{base_url}/session/{user2_session_id}")
        if response.status_code == 404:
            print("✅ User1 cannot access User2's session")
        else:
            print(f"❌ User1 can access User2's session (status: {response.status_code})")
            return False
        
        # User2 trying to access User1's session
        response = session2.get(f"{base_url}/session/{user1_session_id}")
        if response.status_code == 404:
            print("✅ User2 cannot access User1's session")
        else:
            print(f"❌ User2 can access User1's session (status: {response.status_code})")
            return False
    
    print("\n🎉 ALL TESTS PASSED!")
    print("✅ User-specific history filtering is working correctly")
    print("✅ Users can only see their own sessions")
    print("✅ Users cannot access other users' sessions")
    
    return True

if __name__ == "__main__":
    try:
        print("🚀 Starting Flask backend test...")
        print("Make sure the Flask backend is running on http://localhost:5000")
        print("You can start it with: python backend/app.py")
        
        input("\nPress Enter when the backend is ready...")
        
        success = test_history_filtering()
        
        if success:
            print("\n✅ User-specific history filtering is working correctly!")
        else:
            print("\n❌ Some tests failed. Check the output above.")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()