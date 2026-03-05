#!/usr/bin/env python3
"""
Debug script to test if new analyses are being saved and showing in history
"""

import requests
import json
import time
import os

def test_analysis_and_history():
    """Test the complete flow: analysis -> database save -> history display"""
    
    print("🧪 TESTING ANALYSIS TO HISTORY FLOW")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    # Step 1: Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        print("✅ Server is running")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not running. Please start with: python backend/app.py")
        return
    
    # Step 2: Get current history count
    try:
        history_response = requests.get(f"{base_url}/history", timeout=10)
        if history_response.status_code == 200:
            # Count sessions in the HTML response (rough estimate)
            history_content = history_response.text
            session_count_before = history_content.count('<tr>') - 1  # Subtract header row
            print(f"📊 Current sessions in history: {session_count_before}")
        else:
            print(f"⚠️ Could not get history page: {history_response.status_code}")
            session_count_before = 0
    except Exception as e:
        print(f"⚠️ Error getting history: {e}")
        session_count_before = 0
    
    # Step 3: Create a test audio file (simple WAV)
    print("\n🎤 Creating test audio file...")
    
    # Create a simple test WAV file
    test_audio_path = "test_speech.wav"
    
    # Generate a simple WAV file with speech-like content
    import wave
    import numpy as np
    
    # Generate a simple tone (simulating speech)
    sample_rate = 16000
    duration = 2  # 2 seconds
    frequency = 440  # A4 note
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Create a more speech-like waveform with multiple frequencies
    wave_data = (np.sin(frequency * 2 * np.pi * t) * 0.3 + 
                 np.sin(frequency * 1.5 * 2 * np.pi * t) * 0.2 + 
                 np.sin(frequency * 0.8 * 2 * np.pi * t) * 0.1)
    
    # Convert to 16-bit integers
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Write WAV file
    with wave.open(test_audio_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    print(f"✅ Created test audio: {test_audio_path}")
    
    # Step 4: Submit analysis
    print("\n📤 Submitting analysis...")
    
    try:
        with open(test_audio_path, 'rb') as audio_file:
            files = {'audio_file': ('test_speech.wav', audio_file, 'audio/wav')}
            
            analysis_response = requests.post(
                f"{base_url}/analyze", 
                files=files,
                timeout=30
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
                print(f"   Transcript: {analysis.get('transcript', 'N/A')[:50]}...")
                
            else:
                print(f"❌ Analysis failed: {result}")
        else:
            print(f"❌ Analysis request failed: {analysis_response.text}")
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
    
    # Step 5: Wait a moment and check history again
    print("\n⏳ Waiting 2 seconds...")
    time.sleep(2)
    
    try:
        history_response = requests.get(f"{base_url}/history", timeout=10)
        if history_response.status_code == 200:
            history_content = history_response.text
            session_count_after = history_content.count('<tr>') - 1  # Subtract header row
            print(f"📊 Sessions in history after analysis: {session_count_after}")
            
            if session_count_after > session_count_before:
                print("🎉 SUCCESS! New session appears in history!")
            else:
                print("⚠️ No new session in history. Possible issues:")
                print("   - Analysis may have failed")
                print("   - Speech recognition may not have worked")
                print("   - Database save may have failed")
                print("   - Browser cache may need refresh")
        else:
            print(f"❌ Could not get updated history: {history_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting updated history: {e}")
    
    # Cleanup
    if os.path.exists(test_audio_path):
        os.remove(test_audio_path)
        print(f"\n🧹 Cleaned up test file: {test_audio_path}")
    
    print("\n" + "=" * 50)
    print("🔍 DEBUGGING TIPS:")
    print("1. Check server logs for 'Analysis saved to database' message")
    print("2. Try refreshing the history page (F5 or Ctrl+R)")
    print("3. Use browser dev tools to check for JavaScript errors")
    print("4. Try the recording feature instead of file upload")
    print("5. Ensure audio contains clear speech (not just tones)")

if __name__ == "__main__":
    test_analysis_and_history()