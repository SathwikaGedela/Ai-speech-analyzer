#!/usr/bin/env python3
"""
Quick system status verification
"""

import requests
import os
import sqlite3

def verify_system():
    """Verify all system components are working"""
    
    print("🔍 SYSTEM STATUS VERIFICATION")
    print("=" * 40)
    
    # 1. Check database
    print("1. 📊 DATABASE STATUS")
    db_path = os.path.join('backend', 'app.db')
    
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM speech_session")
            count = cursor.fetchone()[0]
            conn.close()
            print(f"   ✅ Database accessible: {count} sessions stored")
        except Exception as e:
            print(f"   ❌ Database error: {e}")
    else:
        print(f"   ❌ Database not found: {db_path}")
    
    # 2. Check server
    print("\n2. 🌐 SERVER STATUS")
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        if response.status_code == 200:
            print("   ✅ Main page accessible")
        else:
            print(f"   ⚠️ Server responded with status: {response.status_code}")
    except requests.exceptions.RequestException:
        print("   ❌ Server not running - start with: python backend/app.py")
        return
    
    # 3. Check history page
    print("\n3. 📜 HISTORY PAGE STATUS")
    try:
        response = requests.get("http://127.0.0.1:5000/history", timeout=5)
        if response.status_code == 200:
            # Count sessions in HTML
            session_count = response.text.count('<tr>') - 1  # Subtract header
            print(f"   ✅ History page accessible: {session_count} sessions displayed")
            
            # Check for charts
            if 'Chart.js' in response.text:
                print("   ✅ Progress charts enabled")
            else:
                print("   ⚠️ Charts may not be loading")
                
        else:
            print(f"   ❌ History page error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ History page error: {e}")
    
    # 4. Check recording feature
    print("\n4. 🎤 RECORDING FEATURE STATUS")
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        if 'navigator.mediaDevices.getUserMedia' in response.text:
            print("   ✅ Recording feature available in UI")
        else:
            print("   ⚠️ Recording feature may not be available")
    except:
        print("   ❌ Could not check recording feature")
    
    print("\n" + "=" * 40)
    print("📋 SUMMARY:")
    print("✅ = Working correctly")
    print("⚠️ = Working but with minor issues") 
    print("❌ = Not working - needs attention")
    
    print("\n💡 RECOMMENDATION:")
    print("If all items show ✅, use the recording feature to test:")
    print("1. Go to http://127.0.0.1:5000")
    print("2. Click 'Start Recording'")
    print("3. Speak for 10-15 seconds")
    print("4. Click 'Stop Recording' → 'Analyze'")
    print("5. Check history page for new entry")

if __name__ == "__main__":
    verify_system()