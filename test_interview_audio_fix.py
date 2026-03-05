#!/usr/bin/env python3
"""
Test Interview Mode Audio Processing with Real Audio
"""

import os
import sys
import requests
import json

# Add backend to path
sys.path.append('backend')

def test_interview_mode_server():
    """Test if interview mode server is running"""
    print("🌐 Testing Interview Mode Server...")
    
    try:
        response = requests.get("http://127.0.0.1:5000/interview", timeout=5)
        if response.status_code == 200:
            print("✅ Interview mode server is running")
            return True
        else:
            print(f"❌ Interview mode server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Interview mode server is not running")
        print("💡 Please start the server with: python backend/app.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False

def create_test_wav_for_interview():
    """Create a test WAV file for interview testing"""
    print("🎵 Creating test WAV for interview...")
    
    try:
        from pydub.generators import Sine
        from pydub import AudioSegment
        
        # Create a 3-second test audio with speech-like characteristics
        # Mix different frequencies to simulate speech
        tone1 = Sine(200).to_audio_segment(duration=1000)  # Low frequency
        tone2 = Sine(400).to_audio_segment(duration=1000)  # Mid frequency
        tone3 = Sine(800).to_audio_segment(duration=1000)  # High frequency
        
        # Combine and reduce volume
        combined = (tone1 + tone2 + tone3).apply_gain(-20)
        
        # Save to file
        test_path = "interview_test.wav"
        combined.export(test_path, format="wav")
        
        print(f"✅ Test WAV created: {test_path} ({len(combined)/1000:.1f}s)")
        return test_path
        
    except Exception as e:
        print(f"❌ Failed to create test WAV: {e}")
        return None

def test_interview_analysis():
    """Test interview analysis with real audio file"""
    print("\n🎤 Testing Interview Analysis...")
    
    # Check if server is running
    if not test_interview_mode_server():
        return False
    
    # Create test audio
    audio_path = create_test_wav_for_interview()
    if not audio_path:
        return False
    
    try:
        # Prepare the request
        url = "http://127.0.0.1:5000/interview/analyze"
        
        # Test data
        data = {
            'question': 'Tell me about yourself.',
            'category': 'hr'
        }
        
        # Upload the file
        with open(audio_path, 'rb') as f:
            files = {'audio_file': ('interview_test.wav', f, 'audio/wav')}
            
            print(f"📤 Uploading {audio_path} to interview analysis...")
            response = requests.post(url, data=data, files=files, timeout=30)
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("✅ Interview analysis successful!")
                
                analysis = result.get('analysis', {})
                print(f"   📝 Question: {analysis.get('question', 'N/A')}")
                print(f"   📊 Confidence: {analysis.get('confidence', 'N/A')}")
                print(f"   ⚡ WPM: {analysis.get('metrics', {}).get('wpm', 'N/A')}")
                print(f"   🎭 Emotion: {analysis.get('emotion', 'N/A')}")
                
                feedback = analysis.get('interview_feedback', {})
                tips = feedback.get('specific_tips', [])
                if tips:
                    print(f"   💡 Tips: {len(tips)} suggestions provided")
                
                return True
            else:
                error = result.get('error', 'Unknown error')
                print(f"❌ Interview analysis failed: {error}")
                return False
        else:
            print(f"❌ Server returned status {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"   Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (analysis took too long)")
        return False
    except Exception as e:
        print(f"❌ Interview analysis test failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(audio_path):
            os.remove(audio_path)

def test_interview_ui():
    """Test interview UI accessibility"""
    print("\n🖥️  Testing Interview UI...")
    
    try:
        response = requests.get("http://127.0.0.1:5000/interview", timeout=5)
        
        if response.status_code == 200:
            content = response.text
            
            # Check for key UI elements
            checks = [
                ("Category selection", "categorySelect" in content),
                ("Question selection", "questionSelect" in content),
                ("Recording section", "recordingSection" in content),
                ("Start recording", "startRecording" in content),
                ("Analyze button", "analyzeAnswer" in content),
                ("File upload", 'type="file"' in content)
            ]
            
            passed = 0
            for check_name, result in checks:
                status = "✅" if result else "❌"
                print(f"   {status} {check_name}")
                if result:
                    passed += 1
            
            if passed == len(checks):
                print("✅ Interview UI is complete")
                return True
            else:
                print(f"⚠️  Interview UI missing {len(checks) - passed} elements")
                return False
        else:
            print(f"❌ Could not load interview UI (status {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Interview UI test failed: {e}")
        return False

def main():
    """Run interview mode tests"""
    print("🎤 Interview Mode Audio Fix Test")
    print("=" * 50)
    
    tests = [
        ("Server Connection", test_interview_mode_server),
        ("Interview UI", test_interview_ui),
        ("Interview Analysis", test_interview_analysis)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 Interview mode is working correctly!")
        print("💡 You can now use interview mode at: http://127.0.0.1:5000/interview")
    else:
        print("⚠️  Some issues found. Check the error messages above.")
        
        if results[0][1] == False:  # Server not running
            print("\n🚀 To start the server:")
            print("   cd backend")
            print("   python app.py")

if __name__ == "__main__":
    main()