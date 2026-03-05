#!/usr/bin/env python3
"""
Test user-specific history filtering
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.session import SpeechSession
import json
from datetime import datetime

def test_user_specific_history():
    """Test that users only see their own history"""
    
    app = create_app()
    
    with app.app_context():
        # Create test users
        user1 = User(
            first_name="Test",
            last_name="User1", 
            email="user1@test.com",
            phone="1234567890"
        )
        user1.set_password("password123")
        
        user2 = User(
            first_name="Test",
            last_name="User2",
            email="user2@test.com", 
            phone="0987654321"
        )
        user2.set_password("password123")
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        print(f"✅ Created test users: {user1.id}, {user2.id}")
        
        # Create sessions for user1
        session1_user1 = SpeechSession(
            user_id=user1.id,
            transcript="Hello this is user 1 session 1",
            wpm=120.0,
            fillers=2,
            sentiment=0.8,
            confidence=85,
            emotion="confident",
            word_count=7,
            created_at=datetime.utcnow()
        )
        
        session2_user1 = SpeechSession(
            user_id=user1.id,
            transcript="Hello this is user 1 session 2", 
            wpm=130.0,
            fillers=1,
            sentiment=0.9,
            confidence=90,
            emotion="happy",
            word_count=7,
            created_at=datetime.utcnow()
        )
        
        # Create sessions for user2
        session1_user2 = SpeechSession(
            user_id=user2.id,
            transcript="Hello this is user 2 session 1",
            wpm=110.0,
            fillers=3,
            sentiment=0.7,
            confidence=75,
            emotion="neutral",
            word_count=7,
            created_at=datetime.utcnow()
        )
        
        session2_user2 = SpeechSession(
            user_id=user2.id,
            transcript="Hello this is user 2 session 2",
            wpm=115.0,
            fillers=2,
            sentiment=0.75,
            confidence=80,
            emotion="calm",
            word_count=7,
            created_at=datetime.utcnow()
        )
        
        db.session.add_all([session1_user1, session2_user1, session1_user2, session2_user2])
        db.session.commit()
        
        print(f"✅ Created test sessions")
        
        # Test client
        client = app.test_client()
        
        # Test user1 history
        with client.session_transaction() as sess:
            sess['user_id'] = user1.id
            
        response = client.get('/api/history')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] == True
        
        user1_sessions = data['sessions']
        print(f"✅ User1 sees {len(user1_sessions)} sessions")
        
        # Verify user1 only sees their own sessions
        assert len(user1_sessions) == 2
        for session in user1_sessions:
            assert "user 1" in session['transcript']
            
        # Test user2 history
        with client.session_transaction() as sess:
            sess['user_id'] = user2.id
            
        response = client.get('/api/history')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] == True
        
        user2_sessions = data['sessions']
        print(f"✅ User2 sees {len(user2_sessions)} sessions")
        
        # Verify user2 only sees their own sessions
        assert len(user2_sessions) == 2
        for session in user2_sessions:
            assert "user 2" in session['transcript']
            
        # Test individual session access
        user1_session_id = user1_sessions[0]['id']
        user2_session_id = user2_sessions[0]['id']
        
        # User1 should be able to access their own session
        with client.session_transaction() as sess:
            sess['user_id'] = user1.id
            
        response = client.get(f'/session/{user1_session_id}')
        assert response.status_code == 200
        print("✅ User1 can access their own session")
        
        # User1 should NOT be able to access user2's session
        response = client.get(f'/session/{user2_session_id}')
        assert response.status_code == 404
        print("✅ User1 cannot access user2's session")
        
        # User2 should be able to access their own session
        with client.session_transaction() as sess:
            sess['user_id'] = user2.id
            
        response = client.get(f'/session/{user2_session_id}')
        assert response.status_code == 200
        print("✅ User2 can access their own session")
        
        # User2 should NOT be able to access user1's session
        response = client.get(f'/session/{user1_session_id}')
        assert response.status_code == 404
        print("✅ User2 cannot access user1's session")
        
        # Test unauthenticated access
        with client.session_transaction() as sess:
            sess.clear()
            
        response = client.get('/api/history')
        assert response.status_code == 401
        print("✅ Unauthenticated users cannot access history")
        
        # Clean up
        db.session.delete(session1_user1)
        db.session.delete(session2_user1)
        db.session.delete(session1_user2)
        db.session.delete(session2_user2)
        db.session.delete(user1)
        db.session.delete(user2)
        db.session.commit()
        
        print("✅ Cleaned up test data")
        
        print("\n🎉 ALL USER-SPECIFIC HISTORY TESTS PASSED!")
        print("✅ Users only see their own sessions")
        print("✅ Users cannot access other users' sessions")
        print("✅ Unauthenticated access is blocked")
        
        return True

if __name__ == "__main__":
    try:
        test_user_specific_history()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()