#!/usr/bin/env python3
"""
Test the new datetime formatting functionality
"""

import sys
import os
sys.path.append('backend')

from backend.app import create_app
from backend.models.session import SpeechSession
from datetime import datetime

def test_datetime_formatting():
    """Test the datetime formatting methods"""
    
    print("🕐 TESTING DATETIME FORMATTING")
    print("=" * 40)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Get existing sessions
        sessions = SpeechSession.query.all()
        
        if not sessions:
            print("❌ No sessions found in database")
            return
        
        print(f"📊 Found {len(sessions)} sessions")
        print("\n🔍 TESTING DIFFERENT FORMATS:")
        
        for i, session in enumerate(sessions[:3], 1):  # Test first 3 sessions
            print(f"\n--- Session {i} ---")
            print(f"Raw UTC time: {session.created_at}")
            print(f"Local time: {session.get_local_time()}")
            print(f"Full format: {session.format_datetime('full')}")
            print(f"Friendly format: {session.format_datetime('friendly')}")
            print(f"Short format: {session.format_datetime('short')}")
            print(f"Chart format: {session.format_datetime('chart')}")
            print(f"Default format: {session.format_datetime()}")
    
    print("\n" + "=" * 40)
    print("✅ Datetime formatting test complete!")
    print("\nThe 'friendly' format will be used in the history table.")
    print("Format: '27 Dec 2025, 10:30' (day month year, hour:minute)")

if __name__ == "__main__":
    test_datetime_formatting()