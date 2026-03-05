#!/usr/bin/env python3
"""
Test database saving with a simulated successful analysis
"""

import sys
import os
import sqlite3

def test_database_saving_logic():
    """Test the database saving logic directly"""
    print("🧪 TESTING DATABASE SAVING LOGIC")
    print("=" * 50)
    
    try:
        # Add backend to path
        sys.path.append('backend')
        
        # Import required modules
        from backend.app import create_app
        from database import db
        from models.session import SpeechSession
        
        # Create app context
        app = create_app()
        
        with app.app_context():
            # Check initial count
            initial_count = SpeechSession.query.count()
            print(f"Initial session count: {initial_count}")
            
            # Create a test session (simulating successful analysis)
            test_session = SpeechSession(
                transcript="Hello everyone, this is a test of the speech analysis system. I am speaking clearly and confidently.",
                wpm=145.0,
                fillers=1,
                sentiment=0.4,
                confidence=88,
                emotion="confident"
            )
            
            # Save to database
            db.session.add(test_session)
            db.session.commit()
            
            print(f"✅ Test session saved with ID: {test_session.id}")
            
            # Check final count
            final_count = SpeechSession.query.count()
            print(f"Final session count: {final_count}")
            print(f"Sessions added: {final_count - initial_count}")
            
            # Get latest sessions
            latest_sessions = SpeechSession.query.order_by(
                SpeechSession.created_at.desc()
            ).limit(3).all()
            
            print("\n📋 Latest sessions in database:")
            for i, session in enumerate(latest_sessions, 1):
                print(f"  {i}. ID {session.id}: {session.transcript[:40]}...")
                print(f"     WPM: {session.wpm}, Confidence: {session.confidence}, Created: {session.created_at}")
            
            print("\n✅ Database saving logic is working correctly!")
            print("💡 The issue might be:")
            print("   1. Speech recognition failing on uploaded audio")
            print("   2. Browser cache not refreshing history page")
            print("   3. Need to refresh history page after successful analysis")
            
            return True
            
    except Exception as e:
        print(f"❌ Database test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_current_database_state():
    """Check current database state"""
    print("\n🔍 CURRENT DATABASE STATE")
    print("=" * 30)
    
    db_path = os.path.join('backend', 'app.db')
    
    if not os.path.exists(db_path):
        print("❌ No database file found")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM speech_session;")
        total_count = cursor.fetchone()[0]
        print(f"Total sessions: {total_count}")
        
        # Get recent sessions
        cursor.execute("""
            SELECT id, transcript, wpm, confidence, emotion, created_at 
            FROM speech_session 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        sessions = cursor.fetchall()
        
        print("\nRecent sessions:")
        for session in sessions:
            session_id, transcript, wpm, confidence, emotion, created_at = session
            print(f"  ID {session_id}: {transcript[:30]}...")
            print(f"    WPM: {wpm}, Confidence: {confidence}, Emotion: {emotion}")
            print(f"    Created: {created_at}")
            print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database check error: {e}")

if __name__ == "__main__":
    check_current_database_state()
    test_database_saving_logic()
    check_current_database_state()