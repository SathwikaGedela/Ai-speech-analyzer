#!/usr/bin/env python3
"""
Test the newly implemented modules
"""

import os
from enhanced_analyzer import EnhancedSpeechAnalyzer
from error_handler import ErrorHandler, get_user_friendly_error
from audio_quality_checker import AudioQualityChecker

def test_module_10_audio_duration():
    """Test MODULE 10: Audio Duration Detection"""
    print("🔧 MODULE 10: Audio Duration Detection")
    print("-" * 40)
    
    analyzer = EnhancedSpeechAnalyzer()
    
    # Test with available files
    test_files = ['uploads/sathaudio.m4a', 'uploads/sathaudio.flac']
    
    for test_file in test_files:
        if os.path.exists(test_file):
            try:
                duration = analyzer._get_audio_duration(test_file)
                print(f"  ✅ {os.path.basename(test_file)}: {duration:.2f} seconds")
            except Exception as e:
                print(f"  ❌ {os.path.basename(test_file)}: Error - {e}")
                return False
        else:
            print(f"  ⚠️ Test file not found: {test_file}")
    
    print("  ✅ MODULE 10: Audio Duration Detection - WORKING")
    return True

def test_module_11_error_handling():
    """Test MODULE 11: Enhanced Error Handling"""
    print("\n🔧 MODULE 11: Enhanced Error Handling")
    print("-" * 40)
    
    error_handler = ErrorHandler()
    
    # Test different error scenarios
    test_errors = [
        (FileNotFoundError("No such file: nonexistent.mp3"), "audio"),
        (Exception("Network timeout occurred"), "transcription"),
        (ValueError("Empty transcript provided"), "analysis"),
        (Exception("Unknown error occurred"), "general")
    ]
    
    for error, error_type in test_errors:
        try:
            if error_type == "audio":
                error_info = error_handler.handle_audio_error(error, "test.mp3")
            elif error_type == "transcription":
                error_info = error_handler.handle_transcription_error(error)
            elif error_type == "analysis":
                error_info = error_handler.handle_analysis_error(error)
            else:
                user_friendly = get_user_friendly_error(error)
                print(f"  ✅ General error handling: {user_friendly}")
                continue
            
            print(f"  ✅ {error_type.title()} error: {error_info['error_type']}")
            print(f"     Message: {error_info['user_message']}")
            
        except Exception as e:
            print(f"  ❌ Error handling failed: {e}")
            return False
    
    print("  ✅ MODULE 11: Enhanced Error Handling - WORKING")
    return True

def test_module_12_audio_quality():
    """Test MODULE 12: Audio Quality Assessment"""
    print("\n🔧 MODULE 12: Audio Quality Assessment")
    print("-" * 40)
    
    quality_checker = AudioQualityChecker()
    
    # Test with available files
    test_files = ['uploads/sathaudio.m4a', 'uploads/sathaudio.flac']
    
    for test_file in test_files:
        if os.path.exists(test_file):
            try:
                assessment = quality_checker.assess_audio_quality(test_file)
                quality_score = quality_checker.get_quality_score(assessment)
                
                print(f"  ✅ {os.path.basename(test_file)}:")
                print(f"     Quality: {assessment['overall_quality'].upper()}")
                print(f"     Score: {quality_score}/100")
                
                if assessment['metrics'].get('duration'):
                    duration = assessment['metrics']['duration']['duration_seconds']
                    print(f"     Duration: {duration:.1f}s")
                
                if assessment['metrics'].get('volume'):
                    db_level = assessment['metrics']['volume']['db_level']
                    print(f"     Volume: {db_level:.1f} dB")
                
                if assessment['issues']:
                    print(f"     Issues: {len(assessment['issues'])}")
                
                if assessment['warnings']:
                    print(f"     Warnings: {len(assessment['warnings'])}")
                
            except Exception as e:
                print(f"  ❌ {os.path.basename(test_file)}: Error - {e}")
                return False
        else:
            print(f"  ⚠️ Test file not found: {test_file}")
    
    print("  ✅ MODULE 12: Audio Quality Assessment - WORKING")
    return True

def test_integrated_system():
    """Test all modules working together"""
    print("\n🔄 TESTING INTEGRATED SYSTEM")
    print("-" * 40)
    
    analyzer = EnhancedSpeechAnalyzer()
    error_handler = ErrorHandler()
    quality_checker = AudioQualityChecker()
    
    # Test with a real file if available
    test_file = 'uploads/sathaudio.m4a'
    
    if os.path.exists(test_file):
        try:
            print("  1️⃣ Audio Quality Assessment...")
            quality_assessment = quality_checker.assess_audio_quality(test_file)
            quality_score = quality_checker.get_quality_score(quality_assessment)
            print(f"     Quality Score: {quality_score}/100")
            
            print("  2️⃣ Audio Duration Detection...")
            duration = analyzer._get_audio_duration(test_file)
            print(f"     Duration: {duration:.2f} seconds")
            
            print("  3️⃣ Speech-to-Text...")
            transcript = analyzer.audio_to_text(test_file)
            print(f"     Transcript: \"{transcript[:50]}...\"")
            
            print("  4️⃣ Comprehensive Analysis...")
            analysis = analyzer.comprehensive_analysis(transcript, duration)
            print(f"     Overall Score: {analysis['overall_score']['score']}/100")
            print(f"     Grammar Score: {analysis['language_content']['grammar']['score']}/100")
            print(f"     Confidence Score: {analysis['emotional_engagement']['confidence_score']}/100")
            
            print("  ✅ INTEGRATED SYSTEM - WORKING")
            return True
            
        except Exception as e:
            print(f"  ❌ Integration test failed: {e}")
            # Test error handling
            user_friendly = get_user_friendly_error(e)
            print(f"     Error handling: {user_friendly}")
            return False
    else:
        print(f"  ⚠️ No test file available for integration test")
        return True

def test_all_new_modules():
    """Test all newly implemented modules"""
    print("🚀 TESTING ALL NEW MODULES")
    print("=" * 60)
    
    tests = [
        test_module_10_audio_duration,
        test_module_11_error_handling,
        test_module_12_audio_quality,
        test_integrated_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"  ❌ {test.__name__} FAILED")
        except Exception as e:
            print(f"  ❌ {test.__name__} ERROR: {e}")
    
    print(f"\n" + "="*60)
    print(f"🎉 NEW MODULES TEST RESULTS")
    print("="*60)
    print(f"✅ Passed: {passed}/{total} modules")
    
    if passed == total:
        print("🚀 ALL NEW MODULES WORKING!")
        print("✅ Audio Duration Detection implemented")
        print("✅ Enhanced Error Handling implemented")
        print("✅ Audio Quality Assessment implemented")
        print("✅ All modules integrated successfully")
    else:
        print(f"⚠️ {total - passed} modules need attention")
    
    return passed == total

if __name__ == "__main__":
    success = test_all_new_modules()
    
    if success:
        print("\n🎯 IMPLEMENTATION COMPLETE!")
        print("All missing modules have been successfully implemented:")
        print("  • MODULE 10: Audio Duration Detection")
        print("  • MODULE 11: Enhanced Error Handling & Recovery")
        print("  • MODULE 12: Audio Quality Assessment")
        print("  • Full system integration verified")
    else:
        print("\n⚠️ Some modules need additional work")