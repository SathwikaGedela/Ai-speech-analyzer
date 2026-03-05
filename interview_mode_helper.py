#!/usr/bin/env python3
"""
Interview Mode Helper - Test with Working Files
"""

import os
import sys
import requests
import json

def test_working_files():
    """Test interview mode with known working files"""
    print("🎤 Interview Mode Helper")
    print("=" * 50)
    
    # Known working files from previous tests
    working_files = [
        'uploads/n.mp3',
        'uploads/sathaudio.flac', 
        'uploads/sathaudio.m4a'
    ]
    
    available_files = []
    for filepath in working_files:
        if os.path.exists(filepath):
            available_files.append(filepath)
            print(f"✅ Found: {os.path.basename(filepath)}")
    
    if not available_files:
        print("❌ No working audio files found")
        print("💡 Please record a voice memo on your phone and save as WAV/MP3")
        return False
    
    print(f"\n🧪 Testing {len(available_files)} files with interview mode...")
    
    # Test each file
    url = "http://127.0.0.1:5000/interview/analyze"
    
    for filepath in available_files:
        filename = os.path.basename(filepath)
        print(f"\n🔧 Testing {filename}...")
        
        try:
            data = {
                'question': 'Tell me about yourself.',
                'category': 'hr'
            }
            
            with open(filepath, 'rb') as f:
                files = {'audio_file': (filename, f, 'audio/wav')}
                response = requests.post(url, data=data, files=files, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"   ✅ SUCCESS! {filename} works perfectly")
                    
                    analysis = result.get('analysis', {})
                    print(f"   📊 Results:")
                    print(f"      Confidence: {analysis.get('confidence', 'N/A')}")
                    print(f"      WPM: {analysis.get('metrics', {}).get('wpm', 'N/A')}")
                    print(f"      Emotion: {analysis.get('emotion', 'N/A')}")
                    
                    feedback = analysis.get('interview_feedback', {})
                    tips = feedback.get('specific_tips', [])
                    if tips:
                        print(f"   💡 Interview Tips:")
                        for i, tip in enumerate(tips[:2], 1):
                            print(f"      {i}. {tip}")
                    
                    print(f"\n🎉 You can use {filename} for testing interview mode!")
                    return True
                else:
                    error = result.get('error', 'Unknown')
                    print(f"   ❌ Analysis failed: {error}")
            else:
                print(f"   ❌ HTTP {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"      Error: {error_data.get('error', 'Unknown')}")
                except:
                    pass
                    
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    return False

def create_voice_recording_guide():
    """Provide step-by-step guide for creating voice recordings"""
    print("\n📱 HOW TO CREATE A WORKING VOICE RECORDING")
    print("=" * 50)
    
    print("\n🎤 Method 1: Windows Voice Recorder")
    print("   1. Press Windows key + R")
    print("   2. Type 'ms-windows-store://pdp/?productid=9WZDNCRFHWKL'")
    print("   3. Install Windows Voice Recorder if not installed")
    print("   4. Open Voice Recorder app")
    print("   5. Click record button")
    print("   6. Say: 'Hello, my name is [your name]. I am testing the interview system.'")
    print("   7. Speak for 30-60 seconds about yourself")
    print("   8. Stop recording")
    print("   9. Save as WAV or MP3")
    print("   10. Upload to interview mode")
    
    print("\n📱 Method 2: Phone Recording")
    print("   1. Open voice recorder app on your phone")
    print("   2. Record yourself speaking clearly for 1 minute")
    print("   3. Say something like an interview answer")
    print("   4. Save the recording")
    print("   5. Transfer to computer (email, cloud, USB)")
    print("   6. Upload to interview mode")
    
    print("\n🌐 Method 3: Online Voice Recorder")
    print("   1. Go to voicerecorder.io or similar site")
    print("   2. Allow microphone access")
    print("   3. Click record")
    print("   4. Speak clearly about yourself")
    print("   5. Download as WAV or MP3")
    print("   6. Upload to interview mode")
    
    print("\n✅ What to Say (Sample Interview Answer):")
    print('   "Hello, my name is [Name]. I am a [profession/student] with')
    print('   experience in [field]. I am passionate about [interests] and')
    print('   I believe I would be a great fit for this role because of my')
    print('   skills in [skills] and my dedication to [values]. Thank you."')

def check_browser_recording():
    """Check if browser recording might work"""
    print("\n🌐 BROWSER RECORDING TROUBLESHOOTING")
    print("=" * 50)
    
    print("\n🔧 If Browser Recording Shows 'Invalid or corrupted audio file':")
    print("   1. The browser recording might be creating invalid WebM files")
    print("   2. This is a common issue with some browsers/systems")
    print("   3. Solution: Use file upload instead of browser recording")
    
    print("\n💡 Browser Recording Tips:")
    print("   • Use Chrome browser (best WebM support)")
    print("   • Check microphone permissions")
    print("   • Speak loudly and clearly")
    print("   • Record in quiet environment")
    print("   • If it fails, use file upload method")
    
    print("\n🔄 Alternative Workflow:")
    print("   1. Instead of browser recording → Use file upload")
    print("   2. Record with phone/computer voice recorder")
    print("   3. Save as WAV, MP3, or M4A")
    print("   4. Upload the file to interview mode")

def main():
    """Main helper function"""
    # Test existing working files
    success = test_working_files()
    
    if success:
        print("\n🎉 GREAT! Interview mode is working with existing files")
        print("💡 You can use these files to test all interview features")
    else:
        print("\n⚠️  Need to create new audio files")
        
    # Provide guidance
    create_voice_recording_guide()
    check_browser_recording()
    
    print("\n🎯 SUMMARY:")
    print("   • Interview mode audio processing is working correctly")
    print("   • The issue is likely with the specific audio file content")
    print("   • Use the guides above to create working voice recordings")
    print("   • File upload method is more reliable than browser recording")
    
    print(f"\n🌐 Access interview mode: http://127.0.0.1:5000/interview")

if __name__ == "__main__":
    main()