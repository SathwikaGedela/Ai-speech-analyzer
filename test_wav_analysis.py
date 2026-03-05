#!/usr/bin/env python3
"""
Test specifically with WAV file
"""

import requests
import os
import time

def test_wav_analysis():
    """Test analysis with WAV file"""
    
    print("🧪 TESTING WITH WAV FILE")
    print("=" * 30)
    
    base_url = "http://127.0.0.1:5000"
    wav_file = "uploads/recorded_speech.wav"
    
    if not os.path.exists(wav_file):
        print(f"❌ WAV file not found: {wav_file}")
        return
    
    print(f"🎵 Using WAV file: {wav_file}")
    print(f"📏 File size: {os.path.getsize(wav_file)} bytes")
    
    # Get current history count
    try:
        history_response = requests.get(f"{base_url}/history", timeout=10)
        session_count_before = history_response.text.count('<tr>') - 1 if history_response.status_code == 200 else 0
        print(f"📊 Current sessions: {session_count_before}")
    except:
        session_count_before = 0
    
    # Submit analysis
    print(f"\n📤 Submitting WAV analysis...")
    
    try:
        with open(wav_file, 'rb') as audio_file:
            files = {'audio_file': ('recorded_speech.wav', audio_file, 'audio/wav')}
            
            print("⏳ Sending request...")
            analysis_response = requests.post(
                f"{base_url}/analyze", 
                files=files,
                timeout=60
            )
        
        print(f"📥 Response status: {analysis_response.status_code}")
        
        if analysis_response.status_code == 200:
            result = analysis_response.json()
            if result.get('success'):
                print("✅ Analysis SUCCESS!")
                
                analysis = result.get('analysis', {})
                print(f"   Transcript: {analysis.get('transcript', 'N/A')[:80]}...")
                print(f"   Confidence: {analysis.get('overall_score', {}).get('score', 'N/A')}")
                
                # Check history immediately
                time.sleep(2)
                history_response = requests.get(f"{base_url}/history", timeout=10)
                session_count_after = history_response.text.count('<tr>') - 1 if history_response.status_code == 200 else 0
                
                print(f"\n📊 Sessions after: {session_count_after}")
                if session_count_after > session_count_before:
                    print("🎉 SUCCESS! History updated!")
                else:
                    print("⚠️ History not updated - check server logs")
                    
            else:
                print(f"❌ Analysis failed: {result}")
        else:
            print(f"❌ Request failed: {analysis_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_wav_analysis()