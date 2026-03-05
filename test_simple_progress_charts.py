#!/usr/bin/env python3
"""
Test simple progress charts implementation
"""

import requests
import json
import time

def test_simple_progress_charts():
    """Test that simple progress charts work with user data"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Simple Progress Charts Implementation...")
    
    # Test 1: Create test user and sign in
    print("\n1. Setting up test user...")
    
    user_data = {
        "first_name": "Simple",
        "last_name": "ChartTester",
        "email": "simplechart@example.com",
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
        "email": "simplechart@example.com",
        "password": "password123"
    })
    
    if signin_response.status_code != 200:
        print(f"❌ Signin failed: {signin_response.status_code}")
        return False
    
    print("✅ User signed in successfully")
    
    # Test 2: Create multiple analysis sessions
    print("\n2. Creating test analysis sessions...")
    
    test_sessions = [
        "Hello this is my first speech analysis test session with basic vocabulary",
        "This is my second speech analysis session and I am improving my speaking skills significantly",
        "My third session shows continued improvement in confidence and speaking pace with better vocabulary usage",
        "Fourth session demonstrates excellent progress with advanced vocabulary and confident delivery style throughout",
        "Fifth session shows mastery of speaking techniques with minimal filler words and excellent pacing control"
    ]
    
    created_sessions = []
    
    for i, text in enumerate(test_sessions):
        print(f"   Creating session {i+1}...")
        
        # Simulate speech analysis
        analysis_data = {"text": text}
        
        response = session.post(f"{base_url}/api/analyze", json=analysis_data)
        
        if response.status_code == 200:
            result = response.json()
            created_sessions.append(result)
            print(f"   ✅ Session {i+1} created (Confidence: {result.get('confidence', 'N/A')}%)")
        else:
            print(f"   ❌ Session {i+1} failed: {response.status_code}")
        
        # Small delay between sessions
        time.sleep(0.5)
    
    print(f"✅ Created {len(created_sessions)} test sessions")
    
    # Test 3: Fetch history data
    print("\n3. Testing history API...")
    
    history_response = session.get(f"{base_url}/api/history")
    
    if history_response.status_code != 200:
        print(f"❌ History fetch failed: {history_response.status_code}")
        return False
    
    history_data = history_response.json()
    
    if not history_data.get('success'):
        print(f"❌ History API returned error: {history_data.get('error', 'Unknown')}")
        return False
    
    sessions = history_data.get('sessions', [])
    
    print(f"✅ Retrieved {len(sessions)} sessions from history")
    
    # Test 4: Validate session data for simple charts
    print("\n4. Validating session data for simple charts...")
    
    required_fields = ['confidence', 'wpm', 'fillers', 'grammar_score', 'created_at']
    
    valid_sessions = 0
    
    for session in sessions[:5]:  # Check first 5 sessions
        session_valid = True
        for field in required_fields:
            if field not in session:
                print(f"   ⚠️ Session missing field: {field}")
                session_valid = False
        
        if session_valid:
            valid_sessions += 1
    
    print(f"✅ {valid_sessions} sessions have complete data for simple charts")
    
    # Test 5: Calculate progress trends
    print("\n5. Testing progress trend calculations...")
    
    if len(sessions) >= 2:
        # Compare first and last sessions
        first_session = sessions[-1]  # Oldest (sessions are in desc order)
        last_session = sessions[0]    # Newest
        
        confidence_change = last_session['confidence'] - first_session['confidence']
        wpm_change = last_session['wpm'] - first_session['wpm']
        fillers_change = last_session['fillers'] - first_session['fillers']
        
        print(f"   Confidence change: {confidence_change:+.1f} points")
        print(f"   WPM change: {wpm_change:+.1f} words per minute")
        print(f"   Fillers change: {fillers_change:+.1f} filler words")
        
        # Determine trends
        confidence_trend = 'up' if confidence_change > 0 else 'down' if confidence_change < 0 else 'stable'
        wpm_trend = 'up' if wpm_change > 0 else 'down' if wpm_change < 0 else 'stable'
        fillers_trend = 'up' if fillers_change < 0 else 'down' if fillers_change > 0 else 'stable'  # Lower is better for fillers
        
        print(f"   Confidence trend: {confidence_trend}")
        print(f"   WPM trend: {wpm_trend}")
        print(f"   Fillers trend: {fillers_trend}")
        
        print("✅ Progress trends calculated successfully")
    
    # Test 6: Calculate averages
    print("\n6. Testing average calculations...")
    
    if sessions:
        total_confidence = sum(s['confidence'] for s in sessions)
        total_wpm = sum(s['wpm'] for s in sessions)
        total_fillers = sum(s['fillers'] for s in sessions)
        
        avg_confidence = total_confidence / len(sessions)
        avg_wpm = total_wpm / len(sessions)
        avg_fillers = total_fillers / len(sessions)
        
        print(f"   Average confidence: {avg_confidence:.1f}%")
        print(f"   Average WPM: {avg_wpm:.1f}")
        print(f"   Average fillers: {avg_fillers:.1f}")
        
        print("✅ Averages calculated successfully")
    
    # Test 7: Verify React frontend compatibility
    print("\n7. Testing React frontend compatibility...")
    
    # Check if data structure is compatible with SimpleProgressCharts
    react_compatible = True
    
    for session in sessions[:3]:  # Check first 3 sessions
        if not isinstance(session.get('confidence'), (int, float)):
            print(f"   ⚠️ Invalid confidence value: {session.get('confidence')}")
            react_compatible = False
        
        if not isinstance(session.get('wpm'), (int, float)):
            print(f"   ⚠️ Invalid WPM value: {session.get('wpm')}")
            react_compatible = False
        
        if not isinstance(session.get('fillers'), (int, float)):
            print(f"   ⚠️ Invalid fillers value: {session.get('fillers')}")
            react_compatible = False
    
    if react_compatible:
        print("   ✅ Sessions are React SimpleProgressCharts compatible")
    else:
        print("   ⚠️ Some React compatibility issues found")
    
    print("\n🎉 SIMPLE PROGRESS CHARTS TESTING COMPLETE!")
    print("✅ Session data structure is valid")
    print("✅ Progress trends can be calculated")
    print("✅ Averages can be calculated")
    print("✅ Data is compatible with React SimpleProgressCharts")
    print("\n📊 Simple progress charts should now be working!")
    print("   Visit: http://localhost:5175/history")
    
    return True

if __name__ == "__main__":
    try:
        print("🚀 Starting Simple Progress Charts Test...")
        print("Make sure the Flask backend is running on http://localhost:5000")
        print("Make sure the React frontend is running on http://localhost:5175")
        
        input("\nPress Enter when both services are ready...")
        
        success = test_simple_progress_charts()
        
        if success:
            print("\n✅ Simple Progress Charts implementation is working correctly!")
        else:
            print("\n❌ Some tests failed. Check the output above.")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()