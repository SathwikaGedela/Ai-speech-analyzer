#!/usr/bin/env python3
"""
Test Interview Mode with Real Audio Files
"""

import os
import sys
import requests
import json

def test_with_real_audio():
    """Test interview analysis with existing audio file"""
    print("🎤 Testing Interview Analysis with Real Audio...")
    
    # Check available audio files
    audio_files = []
    if os.path.exists("uploads"):
        for file in os.listdir("uploads"):
            if file.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
                audio_files.append(os.path.join("uploads", file))
    
    if not audio_files:
        print("❌ No audio files found in uploads directory")
        return False
    
    # Use the first available audio file
    audio_path = audio_files[0]
    print(f"📁 Using audio file: {audio_path}")
    
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
            filename = os.path.basename(audio_path)
            files = {'audio_file': (filename, f, 'audio/wav')}
            
            print(f"📤 Uploading {filename} to interview analysis...")
            response = requests.post(url, data=data, files=files, timeout=60)
        
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
                print(f"   📝 Transcript: {analysis.get('transcript', 'N/A')[:100]}...")
                
                feedback = analysis.get('interview_feedback', {})
                tips = feedback.get('specific_tips', [])
                if tips:
                    print(f"   💡 Interview Tips:")
                    for i, tip in enumerate(tips[:3], 1):
                        print(f"      {i}. {tip}")
                
                return True
            else:
                error = result.get('error', 'Unknown error')
                print(f"❌ Interview analysis failed: {error}")
                
                # Provide helpful suggestions based on error
                if "speech recognition" in error.lower():
                    print("💡 This might be because:")
                    print("   - Audio quality is too low")
                    print("   - No clear speech in the audio")
                    print("   - Audio format issues")
                elif "ffmpeg" in error.lower():
                    print("💡 FFmpeg issue - try using a WAV file")
                
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

def test_multiple_audio_formats():
    """Test different audio formats"""
    print("\n🎵 Testing Multiple Audio Formats...")
    
    if not os.path.exists("uploads"):
        print("❌ No uploads directory found")
        return False
    
    formats_tested = {}
    
    for file in os.listdir("uploads"):
        if file.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
            ext = os.path.splitext(file)[1].lower()
            
            if ext not in formats_tested:
                print(f"\n🔧 Testing {ext.upper()} format with {file}...")
                
                try:
                    url = "http://127.0.0.1:5000/interview/analyze"
                    data = {
                        'question': 'What are your strengths?',
                        'category': 'hr'
                    }
                    
                    with open(os.path.join("uploads", file), 'rb') as f:
                        files = {'audio_file': (file, f, f'audio/{ext[1:]}')}
                        response = requests.post(url, data=data, files=files, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            print(f"   ✅ {ext.upper()} format works")
                            formats_tested[ext] = True
                        else:
                            print(f"   ❌ {ext.upper()} format failed: {result.get('error', 'Unknown')}")
                            formats_tested[ext] = False
                    else:
                        print(f"   ❌ {ext.upper()} format failed: HTTP {response.status_code}")
                        formats_tested[ext] = False
                        
                except Exception as e:
                    print(f"   ❌ {ext.upper()} format failed: {e}")
                    formats_tested[ext] = False
    
    print(f"\n📊 Format Test Results:")
    for ext, result in formats_tested.items():
        status = "✅" if result else "❌"
        print(f"   {status} {ext.upper()} format")
    
    return any(formats_tested.values())

def main():
    """Run real audio tests"""
    print("🎤 Interview Mode Real Audio Test")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://127.0.0.1:5000/interview", timeout=5)
        if response.status_code != 200:
            print("❌ Interview server not running")
            print("💡 Start with: python backend/app.py")
            return
    except:
        print("❌ Interview server not running")
        print("💡 Start with: python backend/app.py")
        return
    
    print("✅ Interview server is running")
    
    # Run tests
    tests = [
        ("Real Audio Analysis", test_with_real_audio),
        ("Multiple Formats", test_multiple_audio_formats)
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
    
    if passed > 0:
        print("🎉 Interview mode audio processing is working!")
        print("💡 Access interview mode at: http://127.0.0.1:5000/interview")
    else:
        print("⚠️  Audio processing issues found.")

if __name__ == "__main__":
    main()