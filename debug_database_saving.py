#!/usr/bin/env python3
"""
Debug database saving issue
"""

import sys
import os
import sqlite3
import subprocess
import time
import requests

def check_database_before_after():
    """Check database before and after a test analysis"""
    print("🔍 DEBUGGING DATABASE SAVING ISSUE")
    print("=" * 50)
    
    db_path = os.path.join('backend', 'app.db')
    
    def get_session_count():
        if not os.path.exists(db_path):
            return 0
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM speech_session;")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_latest_sessions(limit=3):
        if not os.path.exists(db_path):
            return []
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, transcript, wpm, confidence, created_at 
                FROM speech_session 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            sessions = cursor.fetchall()
            conn.close()
            return sessions
        except:
            return []
    
    # Check initial state
    print("\n1️⃣ INITIAL DATABASE STATE")
    print("-" * 30)
    initial_count = get_session_count()
    print(f"Initial session count: {initial_count}")
    
    initial_sessions = get_latest_sessions()
    if initial_sessions:
        print("Latest sessions:")
        for session in initial_sessions:
            session_id, transcript, wpm, confidence, created_at = session
            print(f"  ID {session_id}: {transcript[:30]}... (WPM: {wpm}, Confidence: {confidence})")
    
    # Start backend
    print("\n2️⃣ STARTING BACKEND")
    print("-" * 30)
    
    process = subprocess.Popen(
        [sys.executable, 'backend/app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    time.sleep(3)
    
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print("❌ Backend failed to start")
        print(f"Error: {stderr}")
        return
    
    print("✅ Backend started")
    
    try:
        # Test analysis request
        print("\n3️⃣ TESTING ANALYSIS REQUEST")
        print("-" * 30)
        
        # Create a simple test request
        test_content = b"test audio content"
        files = {'audio_file': ('test.wav', test_content, 'audio/wav')}
        
        print("Sending analysis request...")
        response = requests.post('http://127.0.0.1:5000/analyze', files=files, timeout=15)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('success'):
                    print("✅ Analysis completed successfully")
                else:
                    print(f"❌ Analysis failed: {data.get('error')}")
            except:
                print("❌ Invalid JSON response")
        elif response.status_code == 400:
            try:
                error_data = response.json()
                print(f"⚠️ Expected error (test audio): {error_data.get('error', 'Unknown')}")
            except:
                print("⚠️ Error response (expected for test audio)")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
        
        # Check database after request
        print("\n4️⃣ DATABASE STATE AFTER REQUEST")
        print("-" * 30)
        
        time.sleep(1)  # Give database time to update
        
        final_count = get_session_count()
        print(f"Final session count: {final_count}")
        print(f"Sessions added: {final_count - initial_count}")
        
        if final_count > initial_count:
            print("✅ New session(s) were saved to database!")
            
            final_sessions = get_latest_sessions()
            print("Latest sessions after request:")
            for session in final_sessions:
                session_id, transcript, wpm, confidence, created_at = session
                print(f"  ID {session_id}: {transcript[:30]}... (WPM: {wmp}, Confidence: {confidence})")
        else:
            print("❌ No new sessions were saved to database")
            print("This explains why history page doesn't update!")
    
    finally:
        # Stop backend
        process.terminate()
        process.wait()
        print("\n✅ Backend stopped")
    
    # Summary
    print("\n5️⃣ DIAGNOSIS")
    print("-" * 30)
    
    if final_count > initial_count:
        print("✅ Database saving is working correctly")
        print("✅ History page should show new sessions")
        print("💡 Try refreshing the history page after analysis")
    else:
        print("❌ Database saving is NOT working")
        print("❌ This is why history page doesn't update")
        print("💡 Need to fix the database saving logic")

if __name__ == "__main__":
    check_database_before_after()