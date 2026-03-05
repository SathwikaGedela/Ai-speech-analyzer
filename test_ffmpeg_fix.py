#!/usr/bin/env python3
"""
Test FFmpeg Configuration and Audio Processing
"""

import os
import sys
import tempfile
from io import BytesIO

# Add backend to path
sys.path.append('backend')

from services.audio_processing import setup_ffmpeg, process_audio
from pydub import AudioSegment

class MockFile:
    """Mock file object for testing"""
    def __init__(self, filename, content=b"fake audio content"):
        self.filename = filename
        self.content = content
        self.position = 0
    
    def save(self, path):
        """Save mock content to file"""
        with open(path, 'wb') as f:
            f.write(self.content)
    
    def read(self, size=-1):
        """Read mock content"""
        if size == -1:
            result = self.content[self.position:]
            self.position = len(self.content)
        else:
            result = self.content[self.position:self.position + size]
            self.position += len(result)
        return result

def test_ffmpeg_setup():
    """Test FFmpeg setup and detection"""
    print("🔧 Testing FFmpeg Setup...")
    
    result = setup_ffmpeg()
    
    if result:
        print("✅ FFmpeg setup successful")
        
        # Test if AudioSegment has the right paths
        if hasattr(AudioSegment, 'converter') and AudioSegment.converter:
            print(f"✅ FFmpeg converter: {AudioSegment.converter}")
        if hasattr(AudioSegment, 'ffmpeg') and AudioSegment.ffmpeg:
            print(f"✅ FFmpeg executable: {AudioSegment.ffmpeg}")
        if hasattr(AudioSegment, 'ffprobe') and AudioSegment.ffprobe:
            print(f"✅ FFprobe executable: {AudioSegment.ffprobe}")
        
        return True
    else:
        print("❌ FFmpeg setup failed")
        return False

def create_test_wav():
    """Create a simple test WAV file"""
    print("🎵 Creating test WAV file...")
    
    try:
        # Create a simple 1-second sine wave
        from pydub.generators import Sine
        
        # Generate 1 second of 440Hz sine wave
        tone = Sine(440).to_audio_segment(duration=1000)
        
        # Save to temporary file
        temp_path = "test_audio.wav"
        tone.export(temp_path, format="wav")
        
        print(f"✅ Test WAV created: {temp_path}")
        return temp_path
    
    except Exception as e:
        print(f"❌ Failed to create test WAV: {e}")
        return None

def test_wav_processing():
    """Test WAV file processing"""
    print("\n🎵 Testing WAV Processing...")
    
    # Create test WAV
    wav_path = create_test_wav()
    if not wav_path:
        return False
    
    try:
        # Create mock file object
        with open(wav_path, 'rb') as f:
            content = f.read()
        
        mock_file = MockFile("test.wav", content)
        
        # Test processing
        result_path, duration = process_audio(mock_file)
        
        print(f"✅ WAV processing successful")
        print(f"   - Result path: {result_path}")
        print(f"   - Duration: {duration:.1f} seconds")
        
        # Clean up
        if os.path.exists(result_path):
            os.remove(result_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
        
        return True
        
    except Exception as e:
        print(f"❌ WAV processing failed: {e}")
        
        # Clean up
        if os.path.exists(wav_path):
            os.remove(wav_path)
        
        return False

def test_webm_processing():
    """Test WebM file processing (interview mode uses this)"""
    print("\n🎤 Testing WebM Processing (Interview Mode)...")
    
    try:
        # Create a mock WebM file (just for testing the path)
        mock_file = MockFile("interview_answer.webm", b"fake webm content")
        
        # This should fail gracefully and give us a helpful error
        try:
            result_path, duration = process_audio(mock_file)
            print("✅ WebM processing successful (unexpected)")
            return True
        except Exception as e:
            error_msg = str(e)
            if "FFmpeg" in error_msg and "WAV" in error_msg:
                print("✅ WebM processing failed with helpful error message:")
                print(f"   Error: {error_msg}")
                return True
            else:
                print(f"❌ WebM processing failed with unclear error: {error_msg}")
                return False
        
    except Exception as e:
        print(f"❌ WebM test setup failed: {e}")
        return False

def main():
    """Run all FFmpeg tests"""
    print("🧪 FFmpeg Configuration Test")
    print("=" * 50)
    
    tests = [
        ("FFmpeg Setup", test_ffmpeg_setup),
        ("WAV Processing", test_wav_processing),
        ("WebM Processing", test_webm_processing)
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
        print("🎉 All tests passed! FFmpeg is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        
        if passed == 0:
            print("\n💡 Troubleshooting Tips:")
            print("   1. Ensure FFmpeg is installed: winget install Gyan.FFmpeg")
            print("   2. Restart your terminal/IDE after installation")
            print("   3. Try using WAV files instead of other formats")

if __name__ == "__main__":
    main()