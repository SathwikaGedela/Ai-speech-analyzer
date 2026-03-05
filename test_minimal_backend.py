#!/usr/bin/env python3
"""
Test minimal backend functionality
"""

import sys
import os
sys.path.append('backend')

def test_imports():
    """Test if all backend imports work"""
    print("🧪 TESTING BACKEND IMPORTS")
    print("=" * 40)
    
    try:
        print("Testing Flask app import...")
        from app import app
        print("✅ Flask app imported")
        
        print("Testing audio processing...")
        from services.audio_processing import process_audio
        print("✅ Audio processing imported")
        
        print("Testing speech to text...")
        from services.speech_to_text import speech_to_text
        print("✅ Speech to text imported")
        
        print("Testing text analysis...")
        from services.text_analysis import analyze_text
        print("✅ Text analysis imported")
        
        print("Testing confidence calculation...")
        from services.confidence import calculate_confidence
        print("✅ Confidence calculation imported")
        
        print("Testing emotion detection...")
        from services.emotion import analyze_emotion
        print("✅ Emotion detection imported")
        
        print("Testing routes...")
        from routes.analyze import analyze_bp
        print("✅ Routes imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n🔧 TESTING DEPENDENCIES")
    print("=" * 40)
    
    dependencies = [
        'flask',
        'werkzeug', 
        'pydub',
        'speech_recognition',
        'textblob',
        'cv2'
    ]
    
    missing = []
    
    for dep in dependencies:
        try:
            if dep == 'cv2':
                import cv2
            else:
                __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - MISSING")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    return True

def test_simple_route():
    """Test if we can create a simple route"""
    print("\n🌐 TESTING SIMPLE ROUTE")
    print("=" * 40)
    
    try:
        from flask import Flask, jsonify
        
        test_app = Flask(__name__)
        
        @test_app.route('/test')
        def test_route():
            return jsonify({'status': 'working'})
        
        print("✅ Simple route created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Route test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 MINIMAL BACKEND TEST")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Imports", test_imports),
        ("Simple Route", test_simple_route)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*10} {test_name} {'='*10}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "="*50)
    print("📋 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All basic tests passed!")
        print("The issue might be in the frontend JavaScript or request handling.")
        print("\n🔍 Next steps:")
        print("1. Check browser developer tools (F12)")
        print("2. Look at Network tab when clicking 'Analyze Audio'")
        print("3. Check Console tab for JavaScript errors")
    else:
        print(f"\n⚠️ {len(results) - passed} tests failed")
        print("Fix the failing components first")

if __name__ == "__main__":
    main()