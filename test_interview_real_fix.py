#!/usr/bin/env python3
"""
Test Interview Mode with Real Working Audio
"""

import os
import sys
import requests
import json

def test_with_working_audio():
    """Test with known working audio files"""
    print("🎤 Testing Interview Mode with Working Audio Files...")
    
    # Check for working audio files from previous tests
    working_files = []
    if os.path.exists("uploads"):
        for file in os.listdir("uploads"):
            # Based on previous tests, these formats worked
            if file.lower().endswith(('.flac', '.m4a', '.mp3')):
                working_files.append(os.path.join("uploads", file))
    
    if not working_files:
        print("❌ No working audio files found")
        print("💡 Please ensure you have some audio files in the uploads directory")
        return False
    
    print(f"📁 Found {len(working_files)} potential working files")
    
    # Test with each working file
    url = "http://127.0.0.1:5000/interview/analyze"
    
    for audio_path in working_files[:3]:  # Test up to 3 files
        filename = os.path.basename(audio_path)
        print(f"\n🔧 Testing with {filename}...")
        
        try:
            data = {
                'question': 'Tell me about yourself.',
                'category': 'hr'
            }
            
            with open(audio_path, 'rb') as f:
                files = {'audio_file': (filename, f, 'audio/wav')}
                response = requests.post(url, data=data, files=files, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"   ✅ {filename} - Analysis successful!")
                    
                    analysis = result.get('analysis', {})
                    print(f"      📊 Confidence: {analysis.get('confidence', 'N/A')}")
                    print(f"      ⚡ WPM: {analysis.get('metrics', {}).get('wpm', 'N/A')}")
                    print(f"      🎭 Emotion: {analysis.get('emotion', 'N/A')}")
                    
                    return True
                else:
                    error = result.get('error', 'Unknown error')
                    print(f"   ⚠️  {filename} - Analysis failed: {error}")
                    
                    # Check if it's a speech recognition issue (not FFmpeg)
                    if "speech" in error.lower():
                        print("      💡 This is likely a speech recognition issue, not FFmpeg")
                    
            else:
                print(f"   ❌ {filename} - HTTP {response.status_code}")
                try:
                    error_data = response.json()
                    error = error_data.get('error', 'Unknown')
                    print(f"      Error: {error}")
                    
                    # Check if we're still getting FFmpeg errors
                    if "FFmpeg" in error:
                        print("      ⚠️  Still getting FFmpeg error - needs more investigation")
                    
                except:
                    pass
                    
        except Exception as e:
            print(f"   ❌ {filename} - Exception: {e}")
    
    return False

def test_browser_recording_simulation():
    """Test what happens with browser recording (WebM)"""
    print("\n🎤 Testing Browser Recording Simulation...")
    
    try:
        # Create a more realistic WebM file structure
        # This is still fake but has a better header
        webm_header = b'\x1a\x45\xdf\xa3'  # Basic WebM/Matroska header
        fake_webm_content = webm_header + b'\x00' * 100  # Minimal fake content
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as f:
            f.write(fake_webm_content)
            webm_path = f.name
        
        url = "http://127.0.0.1:5000/interview/analyze"
        data = {
            'question': 'What are your strengths?',
            'category': 'hr'
        }
        
        with open(webm_path, 'rb') as f:
            files = {'audio_file': ('browser_recording.webm', f, 'audio/webm')}
            response = requests.post(url, data=data, files=files, timeout=30)
        
        os.unlink(webm_path)
        
        if response.status_code == 400:
            result = response.json()
            error = result.get('error', '')
            
            print(f"   📝 Error message: {error}")
            
            # Check if we get the improved error message
            if "WebM file processing failed" in error or "recording again" in error:
                print("   ✅ Improved WebM error handling working")
                return True
            elif "corrupted" in error or "invalid" in error:
                print("   ✅ Better error detection working")
                return True
            else:
                print("   ⚠️  Generic error message")
                return False
        else:
            print(f"   ❌ Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ WebM test failed: {e}")
        return False

def test_server_status():
    """Check if server is running and accessible"""
    print("🌐 Checking Server Status...")
    
    try:
        response = requests.get("http://127.0.0.1:5000/interview", timeout=5)
        if response.status_code == 200:
            print("   ✅ Interview server is running")
            
            # Check if the improved UI is there
            content = response.text
            if "Recording Tips" in content:
                print("   ✅ Improved UI with tips is active")
            
            return True
        else:
            print(f"   ❌ Server returned {response.status_code}")
            return False
    except:
        print("   ❌ Server not accessible")
        print("   💡 Start with: python backend/app.py")
        return False

def main():
    """Test the interview mode fixes"""
    print("🎤 Interview Mode Real Fix Test")
    print("=" * 50)
    
    # Check server first
    if not test_server_status():
        return
    
    tests = [
        ("Working Audio Files", test_with_working_audio),
        ("Browser Recording Simulation", test_browser_recording_simulation)
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
        print("🎉 Interview mode improvements are working!")
        print("\n💡 What to try:")
        print("   1. Use the browser recording feature")
        print("   2. Upload MP3, FLAC, or M4A files")
        print("   3. Ensure audio contains clear speech")
        print("   4. Check error messages for specific guidance")
    else:
        print("⚠️  Issues still present - check the error messages above")

if __name__ == "__main__":
    main()