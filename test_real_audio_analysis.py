#!/usr/bin/env python3
"""
Test with real audio file to verify the complete flow
"""

import requests
import os
import time

def test_with_real_audio():
    """Test analysis with existing audio file"""
    
    print("🧪 TESTING WITH REAL AUDIO FILE")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:5000"
    
    # Check available audio files
    audio_files = []
    if os.path.exists('uploads'):
        for file in os.listdir('uploads'):
            if file.endswith(('.wav', '.mp3', '.m4a', '.flac')):
                audio_files.append(os.path.join('uploads', file))
    
    if not audio_files:
        print("❌ No audio files found in uploads folder")
        return
    
    # Use the first available audio file
    test_file = audio_files[0]
    print(f"🎵 Using audio file: {test_file}")
    
    # Get current history count
    try:
        history_response = requests.get(f"{base_url}/history", timeout=10)
        if history_response.status_code == 200:
            history_content = history_response.text
            session_count_before = history_content.count('<tr>') - 1
            print(f"📊 Current sessions in history: {session_count_before}")
        else:
            print(f"⚠️ Could not get history page: {history_response.status_code}")
            session_count_before = 0
    except Exception as e:
        print(f"⚠️ Error getting history: {e}")
        session_count_before = 0
    
    # Submit analysis
    print(f"\n📤 Submitting analysis for: {os.path.basename(test_file)}")
    
    try:
        with open(test_file, 'rb') as audio_file:
            files = {'audio_file': (os.path.basename(test_file), audio_file, 'audio/wav')}
            
            analysis_response = requests.post(
                f"{base_url}/analyze", 
                files=files,
                timeout=60  # Longer timeout for real audio processing
            )
        
        print(f"📥 Analysis response status: {analysis_response.status_code}")
        
        if analysis_response.status_code == 200:
            result = analysis_response.json()
            if result.get('success'):
                print("✅ Analysis completed successfully!")
                
                # Show key metrics
                analysis = result.get('analysis', {})
                overall = analysis.get('overall_score', {})
                vocal = analysis.get('vocal_delivery', {})
                
                print(f"   Confidence: {overall.get('score', 'N/A')}")
                print(f"   WPM: {vocal.get('speaking_pace', {}).get('wpm', 'N/A')}")
                print(f"   Transcript: {analysis.get('transcript', 'N/A')[:100]}...")
                
            else:
                print(f"❌ Analysis failed: {result}")
                return
        else:
            error_text = analysis_response.text
            print(f"❌ Analysis request failed ({analysis_response.status_code}): {error_text}")
            return
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return
    
    # Wait and check history
    print("\n⏳ Waiting 3 seconds for database save...")
    time.sleep(3)
    
    try:
        history_response = requests.get(f"{base_url}/history", timeout=10)
        if history_response.status_code == 200:
            history_content = history_response.text
            session_count_after = history_content.count('<tr>') - 1
            print(f"📊 Sessions in history after analysis: {session_count_after}")
            
            if session_count_after > session_count_before:
                print("🎉 SUCCESS! New session appears in history!")
                print("✅ The history update functionality is working correctly!")
            else:
                print("⚠️ No new session in history.")
                print("\n🔍 POSSIBLE CAUSES:")
                print("1. Speech recognition failed (no clear speech detected)")
                print("2. Database save failed (check server logs)")
                print("3. Browser cache (try hard refresh: Ctrl+Shift+R)")
                print("4. The audio file may not contain recognizable speech")
                
                # Check if there's an error in the response
                if "Could not detect speech" in error_text if 'error_text' in locals() else "":
                    print("5. ✅ CONFIRMED: Speech recognition failed - this is expected for music files")
        else:
            print(f"❌ Could not get updated history: {history_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting updated history: {e}")
    
    print("\n" + "=" * 40)
    print("💡 RECOMMENDATIONS:")
    print("1. For testing, use the recording feature in the web interface")
    print("2. Record yourself speaking clearly for 10-15 seconds")
    print("3. Say something like: 'Hello, this is a test of my speaking skills'")
    print("4. After analysis, refresh the history page to see the new entry")

if __name__ == "__main__":
    test_with_real_audio()