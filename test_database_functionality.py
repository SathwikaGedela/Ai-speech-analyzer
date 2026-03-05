#!/usr/bin/env python3
"""
Test database functionality directly
"""

import sys
import os
sys.path.append('backend')

def test_database_functionality():
    """Test database functionality"""
    print("🧪 TESTING DATABASE FUNCTIONALITY")
    print("=" * 50)
    
    try:
        # Import Flask app
        from backend.app import create_app
        from database import db
        from models.user import User
        from models.session import SpeechSession
        
        print("✅ Imports successful")
        
        # Create app and context
        app = create_app()
        
        with app.app_context():
            print("✅ App context created")
            
            # Create tables
            db.create_all()
            print("✅ Tables created")
            
            # Test creating a speech session
            test_session = SpeechSession(
                transcript="This is a test speech for database functionality.",
                wpm=150.5,
                fillers=2,
                sentiment=0.3,
                confidence=85,
                emotion="confident"
            )
            
            # Save to database
            db.session.add(test_session)
            db.session.commit()
            
            print(f"✅ Test session saved (ID: {test_session.id})")
            
            # Query the session back
            saved_session = SpeechSession.query.first()
            
            if saved_session:
                print("✅ Session retrieved from database:")
                print(f"   ID: {saved_session.id}")
                print(f"   Transcript: {saved_session.transcript[:30]}...")
                print(f"   WPM: {saved_session.wpm}")
                print(f"   Fillers: {saved_session.fillers}")
                print(f"   Confidence: {saved_session.confidence}")
                print(f"   Emotion: {saved_session.emotion}")
                print(f"   Created: {saved_session.created_at}")
            else:
                print("❌ Could not retrieve session")
                return False
            
            # Test user creation
            test_user = User(email="test@example.com")
            db.session.add(test_user)
            db.session.commit()
            
            print(f"✅ Test user created (ID: {test_user.id})")
            
            # Create session with user
            user_session = SpeechSession(
                user_id=test_user.id,
                transcript="This is a user's speech session.",
                wpm=140.0,
                fillers=1,
                sentiment=0.5,
                confidence=90,
                emotion="engaged"
            )
            
            db.session.add(user_session)
            db.session.commit()
            
            print(f"✅ User session saved (ID: {user_session.id})")
            
            # Query all sessions
            all_sessions = SpeechSession.query.all()
            print(f"✅ Total sessions in database: {len(all_sessions)}")
            
            # Test database relationships
            user_sessions = SpeechSession.query.filter_by(user_id=test_user.id).all()
            print(f"✅ Sessions for user {test_user.id}: {len(user_sessions)}")
            
        print("\n🎉 DATABASE FUNCTIONALITY TEST COMPLETE!")
        print("=" * 50)
        print("✅ Tables created successfully")
        print("✅ Speech sessions can be saved and retrieved")
        print("✅ Users can be created")
        print("✅ User-session relationships work")
        print("✅ Database operations are working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_functionality()
    
    if success:
        print("\n🚀 PHASE 4 DATABASE READY!")
        print("Your system now has persistent storage!")
    else:
        print("\n⚠️ Database issues found - check errors above")