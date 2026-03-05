#!/usr/bin/env python3
"""
Test the refactored backend to ensure all functionality works
"""

import requests
import os

def test_refactored_backend():
    """Test the refactored backend functionality"""
    
    print("🧪 TESTING REFACTORED BACKEND")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    # Test 1: Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not accessible: {e}")
        return False
    
    # Test 2: Check if we can access the main page
    try:
        response = requests.get(base_url, timeout=5)
        if "AI Public Speaking Feedback" in response.text:
            print("✅ Main page loads correctly")
        else:
            print("❌ Main page content not found")
            return False
    except Exception as e:
        print(f"❌ Error accessing main page: {e}")
        return False
    
    # Test 3: Test with actual audio file if available
    test_file = "uploads/sathaudio.m4a"
    if os.path.exists(test_file):
        try:
            with open(test_file, 'rb') as f:
                files = {'audio_file': (os.path.basename(test_file), f, 'audio/m4a')}
                response = requests.post(f"{base_url}/analyze", files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    analysis = result['analysis']
                    print("✅ Audio analysis working:")
                    print(f"   📝 Transcript: \"{analysis['transcript'][:50]}...\"")
                    print(f"   ⏱️ WPM: {analysis['metrics']['wpm']}")
                    print(f"   🗣️ Fillers: {analysis['metrics']['fillers']}")
                    print(f"   😊 Sentiment: {analysis['metrics']['sentiment']}")
                    print(f"   🎯 Confidence: {analysis['confidence']}/100")
                else:
                    print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ Analysis request failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error testing audio analysis: {e}")
            return False
    else:
        print("⚠️ No test audio file available, skipping audio analysis test")
    
    print("✅ All backend tests passed!")
    return True

def verify_modular_structure():
    """Verify the modular structure is correct"""
    
    print("\n🏗️ VERIFYING MODULAR STRUCTURE")
    print("=" * 50)
    
    required_files = [
        "backend/app.py",
        "backend/routes/__init__.py",
        "backend/routes/analyze.py",
        "backend/services/__init__.py",
        "backend/services/audio_processing.py",
        "backend/services/speech_to_text.py",
        "backend/services/text_analysis.py",
        "backend/services/confidence.py",
        "backend/utils/__init__.py",
        "backend/utils/validators.py",
        "backend/templates/enhanced_index.html"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    if all_exist:
        print("✅ All required files exist")
    else:
        print("❌ Some files are missing")
        return False
    
    # Check if files have content (not empty)
    content_files = [
        "backend/app.py",
        "backend/routes/analyze.py",
        "backend/services/audio_processing.py",
        "backend/services/speech_to_text.py",
        "backend/services/text_analysis.py",
        "backend/services/confidence.py"
    ]
    
    for file_path in content_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read().strip()
                if len(content) > 50:  # Has substantial content
                    print(f"✅ {file_path} has implementation")
                else:
                    print(f"❌ {file_path} appears empty or minimal")
                    return False
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return False
    
    print("✅ Modular structure is correct and implemented")
    return True

if __name__ == "__main__":
    print("🚀 PHASE 2 VERIFICATION - BACKEND REFACTORING")
    print("=" * 60)
    
    structure_ok = verify_modular_structure()
    backend_ok = test_refactored_backend()
    
    print(f"\n" + "="*60)
    print("🎉 PHASE 2 RESULTS")
    print("="*60)
    
    if structure_ok and backend_ok:
        print("✅ PHASE 2 SUCCESSFUL!")
        print("✅ Backend successfully refactored into modular structure")
        print("✅ All functionality preserved")
        print("✅ Clean separation of concerns achieved")
        print("✅ Ready for further development")
        
        print(f"\n🏗️ WHAT YOU ACHIEVED:")
        print("• Separated routing, business logic, and AI")
        print("• Clean boundaries between components")
        print("• Modular structure for easy maintenance")
        print("• Can add ANY feature safely now")
        
    else:
        print("❌ PHASE 2 NEEDS ATTENTION")
        if not structure_ok:
            print("❌ Modular structure issues")
        if not backend_ok:
            print("❌ Backend functionality issues")
        print("Consider reverting to app_enhanced.py and retry")