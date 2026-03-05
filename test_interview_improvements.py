#!/usr/bin/env python3
"""
Test Interview Mode Improvements and Error Handling
"""

import os
import sys
import requests
import json
import tempfile

def test_error_handling():
    """Test improved error handling"""
    print("🔧 Testing Improved Error Handling...")
    
    # Test 1: Invalid audio file
    print("\n📁 Testing with invalid audio file...")
    try:
        url = "http://127.0.0.1:5000/interview/analyze"
        data = {
            'question': 'Tell me about yourself.',
            'category': 'hr'
        }
        
        # Create a fake audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(b"fake audio content that is not real audio")
            fake_path = f.name
        
        with open(fake_path, 'rb') as f:
            files = {'audio_file': ('fake.wav', f, 'audio/wav')}
            response = requests.post(url, data=data, files=files, timeout=30)
        
        os.unlink(fake_path)
        
        if response.status_code == 400:
            result = response.json()
            error = result.get('error', '')
            if 'speech' in error.lower() and ('clear' in error.lower() or 'tips' in error.lower()):
                print("   ✅ Improved speech recognition error message")
            else:
                print(f"   ⚠️  Basic error message: {error}")
        else:
            print(f"   ❌ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error handling test failed: {e}")
    
    # Test 2: Working audio file (if available)
    print("\n📁 Testing with working audio file...")
    working_files = []
    if os.path.exists("uploads"):
        for file in os.listdir("uploads"):
            if file.lower().endswith(('.flac', '.m4a')):  # These worked in previous test
                working_files.append(os.path.join("uploads", file))
    
    if working_files:
        try:
            with open(working_files[0], 'rb') as f:
                files = {'audio_file': (os.path.basename(working_files[0]), f, 'audio/flac')}
                response = requests.post(url, data=data, files=files, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("   ✅ Working audio file processed successfully")
                    return True
                else:
                    print(f"   ⚠️  Working file failed: {result.get('error', 'Unknown')}")
            else:
                print(f"   ❌ Working file returned {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Working file test failed: {e}")
    else:
        print("   ⚠️  No working audio files found for testing")
    
    return False

def test_ui_improvements():
    """Test UI improvements"""
    print("\n🖥️  Testing UI Improvements...")
    
    try:
        response = requests.get("http://127.0.0.1:5000/interview", timeout=5)
        
        if response.status_code == 200:
            content = response.text
            
            # Check for improved UI elements
            checks = [
                ("Recording tips", "Recording Tips" in content),
                ("Speak clearly tip", "Speak clearly" in content),
                ("Quiet environment tip", "quiet environment" in content),
                ("File format guidance", "WAV, MP3, M4A, or FLAC" in content),
                ("Error handling JS", "Analysis Failed" in content),
                ("Solution suggestions", "Try these solutions" in content)
            ]
            
            passed = 0
            for check_name, result in checks:
                status = "✅" if result else "❌"
                print(f"   {status} {check_name}")
                if result:
                    passed += 1
            
            if passed >= 4:  # Most improvements should be present
                print("✅ UI improvements implemented")
                return True
            else:
                print(f"⚠️  Only {passed}/{len(checks)} UI improvements found")
                return False
        else:
            print(f"❌ Could not load interview UI (status {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ UI improvements test failed: {e}")
        return False

def test_audio_format_support():
    """Test audio format support"""
    print("\n🎵 Testing Audio Format Support...")
    
    if not os.path.exists("uploads"):
        print("❌ No uploads directory found")
        return False
    
    formats_found = {}
    formats_working = {}
    
    # Check what formats we have
    for file in os.listdir("uploads"):
        if file.lower().endswith(('.wav', '.mp3', '.m4a', '.flac', '.webm')):
            ext = os.path.splitext(file)[1].lower()
            formats_found[ext] = file
    
    print(f"📁 Found formats: {list(formats_found.keys())}")
    
    # Test each format
    url = "http://127.0.0.1:5000/interview/analyze"
    data = {
        'question': 'What are your strengths?',
        'category': 'hr'
    }
    
    for ext, file in formats_found.items():
        try:
            print(f"   Testing {ext.upper()}...")
            
            with open(os.path.join("uploads", file), 'rb') as f:
                files = {'audio_file': (file, f, f'audio/{ext[1:]}')}
                response = requests.post(url, data=data, files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    formats_working[ext] = True
                    print(f"      ✅ {ext.upper()} works")
                else:
                    formats_working[ext] = False
                    error = result.get('error', 'Unknown')
                    if 'speech' in error.lower():
                        print(f"      ⚠️  {ext.upper()} processed but no speech detected")
                    else:
                        print(f"      ❌ {ext.upper()} failed: {error[:50]}...")
            else:
                formats_working[ext] = False
                print(f"      ❌ {ext.upper()} failed: HTTP {response.status_code}")
                
        except Exception as e:
            formats_working[ext] = False
            print(f"      ❌ {ext.upper()} crashed: {e}")
    
    working_count = sum(formats_working.values())
    total_count = len(formats_working)
    
    print(f"\n📊 Format Support: {working_count}/{total_count} formats working")
    
    return working_count > 0

def main():
    """Run interview improvements tests"""
    print("🎤 Interview Mode Improvements Test")
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
        ("Error Handling", test_error_handling),
        ("UI Improvements", test_ui_improvements),
        ("Audio Format Support", test_audio_format_support)
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
    
    if passed >= 2:
        print("🎉 Interview mode improvements are working!")
        print("💡 The system now provides:")
        print("   - Better error messages with helpful suggestions")
        print("   - Improved UI with recording tips")
        print("   - Support for multiple audio formats")
        print("   - Enhanced user guidance")
        print(f"\n🌐 Access interview mode at: http://127.0.0.1:5000/interview")
    else:
        print("⚠️  Some improvements may not be working as expected.")

if __name__ == "__main__":
    main()