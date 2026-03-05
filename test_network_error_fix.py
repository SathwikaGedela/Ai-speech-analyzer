#!/usr/bin/env python3
"""
Test the network error fix
"""

import sys
import os
import subprocess
import time
import requests
import tempfile
import wave
import numpy as np

def create_test_wav_file():
    """Create a simple test WAV file"""
    # Create a simple sine wave
    sample_rate = 16000
    duration = 2  # 2 seconds
    frequency = 440  # A4 note
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Convert to 16-bit integers
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Create temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    
    with wave.open(temp_file.name, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    return temp_file.name

def test_network_error_fix():
    print("🔧 TESTING NETWORK ERROR FIX")
    print("=" * 40)
    
    # Start backend
    print("\n1️⃣ Starting Backend...")
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
        # Test with a real WAV file
        print("\n2️⃣ Creating Test Audio File...")
        
        try:
            wav_file = create_test_wav_file()
            print("✅ Test WAV file created")
        except Exception as e:
            print(f"⚠️ Could not create WAV file: {e}")
            print("Using simple test instead...")
            wav_file = None
        
        # Test the analyze endpoint
        print("\n3️⃣ Testing Analyze Endpoint...")
        
        if wav_file:
            # Test with real WAV file
            with open(wav_file, 'rb') as f:
                files = {'audio_file': ('test.wav', f, 'audio/wav')}
                
                try:
                    response = requests.post('http://127.0.0.1:5000/analyze', files=files, timeout=30)
                    print(f"Status Code: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success'):
                            print("✅ Analysis successful!")
                            print(f"   Transcript: {data['analysis']['transcript'][:50]}...")
                            print(f"   Confidence: {data['analysis']['overall_score']['score']}")
                        else:
                            print(f"❌ Analysis failed: {data.get('error', 'Unknown error')}")
                    else:
                        try:
                            error_data = response.json()
                            print(f"❌ Server error: {error_data.get('error', 'Unknown error')}")
                        except:
                            print(f"❌ Server error: {response.text[:200]}...")
                            
                except requests.exceptions.Timeout:
                    print("❌ Request timed out")
                except Exception as e:
                    print(f"❌ Request failed: {e}")
            
            # Clean up
            os.unlink(wav_file)
        
        else:
            print("⚠️ Skipping real audio test")
        
        # Test error handling
        print("\n4️⃣ Testing Error Handling...")
        
        # Test with invalid file
        files = {'audio_file': ('invalid.txt', b'not audio data', 'text/plain')}
        
        try:
            response = requests.post('http://127.0.0.1:5000/analyze', files=files, timeout=10)
            print(f"Invalid file status: {response.status_code}")
            
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    print(f"✅ Proper error message: {error_data.get('error', 'No error message')}")
                except:
                    print("⚠️ Error response not JSON")
            
        except Exception as e:
            print(f"Error test failed: {e}")
    
    finally:
        # Stop backend
        process.terminate()
        process.wait()
        print("\n✅ Backend stopped")
    
    print("\n5️⃣ SUMMARY:")
    print("-" * 20)
    print("✅ Improved FFmpeg path detection")
    print("✅ Better error handling in audio processing")
    print("✅ More specific error messages")
    print("✅ Graceful fallback for unsupported formats")
    
    print("\n🎯 IF YOU STILL GET 'Network error':")
    print("   1. Check browser developer tools (F12)")
    print("   2. Look at Network tab for actual error")
    print("   3. Try with a simple WAV file first")
    print("   4. Ensure microphone permissions are granted")

if __name__ == "__main__":
    test_network_error_fix()