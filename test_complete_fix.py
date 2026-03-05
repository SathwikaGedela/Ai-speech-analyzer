#!/usr/bin/env python3
"""
Test the complete fix for the Network error
"""

import sys
import os
import subprocess
import time
import requests
import tempfile
import wave
import numpy as np

def create_simple_wav():
    """Create a simple test WAV file"""
    try:
        # Create a simple sine wave
        sample_rate = 16000
        duration = 3  # 3 seconds
        frequency = 440  # A4 note
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave_data = np.sin(2 * np.pi * frequency * t) * 0.3
        wave_data = (wave_data * 32767).astype(np.int16)
        
        # Create temporary WAV file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        
        with wave.open(temp_file.name, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(wave_data.tobytes())
        
        return temp_file.name
    except:
        return None

def test_complete_system():
    print("🔧 TESTING COMPLETE NETWORK ERROR FIX")
    print("=" * 50)
    
    # Test imports first
    print("\n1️⃣ Testing Backend Imports...")
    try:
        sys.path.append('backend')
        from services.text_analysis import analyze_text
        from services.confidence import calculate_confidence
        from routes.analyze import get_skill_level, generate_strengths
        
        print("✅ All imports successful")
        
        # Test text analysis
        test_text = "Hello everyone, this is a test speech."
        metrics = analyze_text(test_text, 5.0)
        confidence = calculate_confidence(metrics)
        
        print(f"✅ Text analysis working: {metrics['wpm']} WPM")
        print(f"✅ Confidence calculation working: {confidence}/100")
        
    except Exception as e:
        print(f"❌ Import/function error: {e}")
        return False
    
    # Start backend
    print("\n2️⃣ Starting Backend...")
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
        return False
    
    print("✅ Backend started successfully")
    
    try:
        # Test main page
        print("\n3️⃣ Testing Main Page...")
        response = requests.get('http://127.0.0.1:5000', timeout=5)
        if response.status_code == 200:
            print("✅ Main page loads successfully")
        else:
            print(f"⚠️ Main page status: {response.status_code}")
        
        # Test with simple audio file
        print("\n4️⃣ Testing Audio Analysis...")
        
        wav_file = create_simple_wav()
        if wav_file:
            print("✅ Test WAV file created")
            
            with open(wav_file, 'rb') as f:
                files = {'audio_file': ('test.wav', f, 'audio/wav')}
                
                try:
                    response = requests.post('http://127.0.0.1:5000/analyze', files=files, timeout=30)
                    
                    print(f"Response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if data.get('success'):
                                print("🎉 ANALYSIS SUCCESSFUL!")
                                print(f"   Transcript: {data['analysis']['transcript'][:50]}...")
                                print(f"   Confidence: {data['analysis']['overall_score']['score']}")
                                print(f"   Skill Level: {data['analysis']['overall_score']['skill_level']}")
                                print(f"   WPM: {data['analysis']['vocal_delivery']['speaking_pace']['wpm']}")
                                print("✅ Complete response structure working!")
                                return True
                            else:
                                print(f"❌ Analysis failed: {data.get('error')}")
                        except Exception as e:
                            print(f"❌ JSON parsing error: {e}")
                            print(f"Response: {response.text[:200]}...")
                    else:
                        try:
                            error_data = response.json()
                            print(f"❌ Server error: {error_data.get('error')}")
                        except:
                            print(f"❌ HTTP error {response.status_code}: {response.text[:200]}...")
                
                except requests.exceptions.Timeout:
                    print("❌ Request timed out")
                except Exception as e:
                    print(f"❌ Request error: {e}")
            
            # Clean up
            os.unlink(wav_file)
        else:
            print("⚠️ Could not create test WAV file")
    
    finally:
        # Stop backend
        process.terminate()
        process.wait()
        print("\n✅ Backend stopped")
    
    return False

if __name__ == "__main__":
    success = test_complete_system()
    
    if success:
        print("\n🎉 NETWORK ERROR FIXED!")
        print("=" * 30)
        print("✅ Backend working correctly")
        print("✅ Complete response format")
        print("✅ All services functional")
        print("\n🚀 TO USE:")
        print("1. Run: python backend/app.py")
        print("2. Open: http://127.0.0.1:5000")
        print("3. Upload audio or record speech")
        print("4. Get comprehensive analysis!")
    else:
        print("\n⚠️ Issues still exist - check the errors above")