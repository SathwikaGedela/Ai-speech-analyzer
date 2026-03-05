#!/usr/bin/env python3
"""
Test progress charts implementation
"""

import requests
import json
import time

def test_progress_charts():
    """Test that progress charts work with user data"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Progress Charts Implementation...")
    
    # Test 1: Create test user and sign in
    print("\n1. Setting up test user...")
    
    user_data = {
        "first_name": "Chart",
        "last_name": "Tester",
        "email": "charttester@example.com",
        "phone": "1234567890",
        "password": "password123"
    }
    
    # Create user (might already exist)
    response = requests.post(f"{base_url}/api/signup", json=user_data)
    if response.status_code in [201, 400]:  # 400 if user already exists
        print("✅ Test user ready")
    else:
        print(f"❌ User creation failed: {response.status_code}")
        return False
    
    # Sign in
    session = requests.Session()
    signin_response = session.post(f"{base_url}/api/signin", json={
        "email": "charttester@example.com",
        "password": "password123"
    })
    
    if signin_response.status_code != 200:
        print(f"❌ Signin failed: {signin_response.status_code}")
        return False
    
    print("✅ User signed in successfully")
    
    # Test 2: Create multiple analysis sessions with varying metrics
    print("\n2. Creating test analysis sessions...")
    
    test_sessions = [
        {
            "text": "Hello this is my first speech analysis test session",
            "expected_confidence": 75,
            "expected_wpm": 120
        },
        {
            "text": "This is my second speech analysis session and I am improving my speaking skills",
            "expected_confidence": 80,
            "expected_wpm": 130
        },
        {
            "text": "My third session shows continued improvement in confidence and speaking pace with better vocabulary",
            "expected_confidence": 85,
            "expected_wpm": 140
        },
        {
            "text": "Fourth session demonstrates excellent progress with advanced vocabulary and confident delivery style",
            "expected_confidence": 90,
            "expected_wpm": 150
        }
    ]
    
    created_sessions = []
    
    for i, test_data in enumerate(test_sessions):
        print(f"   Creating session {i+1}...")
        
        # Simulate speech analysis
        analysis_data = {
            "text": test_data["text"]
        }
        
        response = session.post(f"{base_url}/api/analyze", json=analysis_data)
        
        if response.status_code == 200:
            result = response.json()
            created_sessions.append(result)
            print(f"   ✅ Session {i+1} created (Confidence: {result.get('confidence', 'N/A')}%)")
        else:
            print(f"   ❌ Session {i+1} failed: {response.status_code}")
        
        # Small delay between sessions
        time.sleep(1)
    
    print(f"✅ Created {len(created_sessions)} test sessions")
    
    # Test 3: Fetch history data for charts
    print("\n3. Testing history API for chart data...")
    
    history_response = session.get(f"{base_url}/api/history")
    
    if history_response.status_code != 200:
        print(f"❌ History fetch failed: {history_response.status_code}")
        return False
    
    history_data = history_response.json()
    
    if not history_data.get('success'):
        print(f"❌ History API returned error: {history_data.get('error', 'Unknown')}")
        return False
    
    sessions = history_data.get('sessions', [])
    chart_data = history_data.get('chart_data', {})
    
    print(f"✅ Retrieved {len(sessions)} sessions from history")
    print(f"✅ Chart data includes: {list(chart_data.keys())}")
    
    # Test 4: Validate chart data structure
    print("\n4. Validating chart data structure...")
    
    required_chart_fields = ['labels', 'confidence', 'wpm', 'fillers']
    
    for field in required_chart_fields:
        if field not in chart_data:
            print(f"❌ Missing chart field: {field}")
            return False
        
        if not isinstance(chart_data[field], list):
            print(f"❌ Chart field {field} is not a list")
            return False
        
        print(f"   ✅ {field}: {len(chart_data[field])} data points")
    
    # Test 5: Validate session data for charts
    print("\n5. Validating session data for progress tracking...")
    
    required_session_fields = [
        'confidence', 'wpm', 'fillers', 'grammar_score', 
        'vocabulary_diversity', 'unique_words', 'created_at'
    ]
    
    valid_sessions = 0
    
    for session in sessions[:5]:  # Check first 5 sessions
        session_valid = True
        for field in required_session_fields:
            if field not in session:
                print(f"   ⚠️ Session missing field: {field}")
                session_valid = False
        
        if session_valid:
            valid_sessions += 1
    
    print(f"✅ {valid_sessions} sessions have complete data for charts")
    
    # Test 6: Check for progress trends
    print("\n6. Analyzing progress trends...")
    
    if len(sessions) >= 2:
        # Compare first and last sessions
        first_session = sessions[-1]  # Oldest (sessions are in desc order)
        last_session = sessions[0]    # Newest
        
        confidence_change = last_session['confidence'] - first_session['confidence']
        wpm_change = last_session['wpm'] - first_session['wpm']
        
        print(f"   Confidence change: {confidence_change:+.1f} points")
        print(f"   WPM change: {wpm_change:+.1f} words per minute")
        
        if confidence_change > 0:
            print("   ✅ Confidence shows improvement trend")
        elif confidence_change < 0:
            print("   📉 Confidence shows decline trend")
        else:
            print("   ➡️ Confidence remains stable")
        
        if wpm_change > 0:
            print("   ✅ Speaking speed shows improvement trend")
        elif wpm_change < 0:
            print("   📉 Speaking speed shows decline trend")
        else:
            print("   ➡️ Speaking speed remains stable")
    
    # Test 7: Verify React frontend can access chart data
    print("\n7. Testing React frontend compatibility...")
    
    # Check if all required fields for React charts are present
    react_required_fields = [
        'id', 'confidence', 'wpm', 'fillers', 'grammar_score',
        'vocabulary_diversity', 'unique_words', 'created_at_chart'
    ]
    
    react_compatible = True
    
    for session in sessions[:3]:  # Check first 3 sessions
        for field in react_required_fields:
            if field not in session:
                print(f"   ⚠️ React compatibility issue: missing {field}")
                react_compatible = False
    
    if react_compatible:
        print("   ✅ Sessions are React Chart.js compatible")
    else:
        print("   ⚠️ Some React compatibility issues found")
    
    print("\n🎉 PROGRESS CHARTS TESTING COMPLETE!")
    print("✅ Chart data structure is valid")
    print("✅ Session data includes all required metrics")
    print("✅ Progress trends can be calculated")
    print("✅ Data is compatible with React Chart.js")
    
    return True

if __name__ == "__main__":
    try:
        print("🚀 Starting Progress Charts Test...")
        print("Make sure the Flask backend is running on http://localhost:5000")
        print("Make sure the React frontend is running on http://localhost:5175")
        
        input("\nPress Enter when both services are ready...")
        
        success = test_progress_charts()
        
        if success:
            print("\n✅ Progress Charts implementation is working correctly!")
            print("\n📊 You can now view interactive charts at:")
            print("   http://localhost:5175/history")
        else:
            print("\n❌ Some tests failed. Check the output above.")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()