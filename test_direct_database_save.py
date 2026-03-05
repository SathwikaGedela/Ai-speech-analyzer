#!/usr/bin/env python3
"""
Test direct database saving to verify the history update functionality
"""

import sys
import os
sys.path.append('backend')

from backend.app import create_app
from backend.database import db
from backend.models.session import SpeechSession
from datetime import datetime

def test_direct_save():
    """Test saving directly to database and verify it appears in history"""
    
    print("🧪 TESTING DIRECT DATABASE SAVE")
    print("=" * 40)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Get current count
        current_count = SpeechSession.query.count()
        print(f"📊 Current sessions in database: {current_count}")
        
        # Create a new test session
        test_session = SpeechSession(
            transcript="This is a test speech to verify history updates are working correctly.",
            wpm=145.0,
            fillers=1,
            sentiment=0.4,
            confidence=88,
            emotion="confident"
        )
        
        try:
            db.session.add(test_session)
            db.session.commit()
            
            new_count = SpeechSession.query.count()
            print(f"✅ Session saved! New count: {new_count}")
            print(f"   Session ID: {test_session.id}")
            print(f"   Created at: {test_session.created_at}")
            
            # Verify the session exists
            saved_session = SpeechSession.query.get(test_session.id)
            if saved_session:
                print(f"✅ Session verified in database")
                print(f"   Transcript: {saved_session.transcript[:50]}...")
                print(f"   Confidence: {saved_session.confidence}")
                print(f"   WPM: {saved_session.wpm}")
            else:
                print(f"❌ Session not found after save")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Database save failed: {e}")
            return
    
    print("\n🌐 TESTING HISTORY PAGE ACCESS")
    print("=" * 40)
    
    # Test history page
    import requests
    
    try:
        response = requests.get("http://127.0.0.1:5000/history", timeout=10)
        
        if response.status_code == 200:
            print("✅ History page accessible")
            
            # Check if our test session appears
            content = response.text
            if "This is a test speech to verify" in content:
                print("🎉 SUCCESS! Test session appears in history page!")
            else:
                print("⚠️ Test session not visible in history page")
                print("   This could be a browser cache issue")
                
            # Count sessions in HTML
            session_rows = content.count('<tr>') - 1  # Subtract header
            print(f"📊 Sessions visible in history page: {session_rows}")
            
        else:
            print(f"❌ History page error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error accessing history page: {e}")
    
    print("\n" + "=" * 40)
    print("🔍 CONCLUSION:")
    print("If the session was saved but not visible in history:")
    print("1. Try hard refresh (Ctrl+Shift+R)")
    print("2. Clear browser cache")
    print("3. Try incognito/private mode")
    print("4. Check browser console for JavaScript errors")

if __name__ == "__main__":
    test_direct_save()