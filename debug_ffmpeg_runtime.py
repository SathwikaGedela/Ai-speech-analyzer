#!/usr/bin/env python3
"""
Debug FFmpeg Runtime Configuration
"""

import os
import sys
import tempfile

# Add backend to path
sys.path.append('backend')

def test_pydub_configuration():
    """Test pydub configuration in detail"""
    print("🔧 Testing pydub Configuration...")
    
    try:
        from pydub import AudioSegment
        
        print(f"   AudioSegment.converter: {getattr(AudioSegment, 'converter', 'Not set')}")
        print(f"   AudioSegment.ffmpeg: {getattr(AudioSegment, 'ffmpeg', 'Not set')}")
        print(f"   AudioSegment.ffprobe: {getattr(AudioSegment, 'ffprobe', 'Not set')}")
        
        # Test if the paths exist
        if hasattr(AudioSegment, 'converter') and AudioSegment.converter:
            exists = os.path.exists(AudioSegment.converter)
            print(f"   Converter exists: {exists}")
        
        if hasattr(AudioSegment, 'ffmpeg') and AudioSegment.ffmpeg:
            exists = os.path.exists(AudioSegment.ffmpeg)
            print(f"   FFmpeg exists: {exists}")
            
        return True
        
    except Exception as e:
        print(f"   ❌ pydub configuration error: {e}")
        return False

def test_audio_processing_import():
    """Test importing audio processing module"""
    print("\n📦 Testing Audio Processing Import...")
    
    try:
        from services.audio_processing import FFMPEG_AVAILABLE, setup_ffmpeg
        
        print(f"   FFMPEG_AVAILABLE: {FFMPEG_AVAILABLE}")
        
        # Test setup function
        result = setup_ffmpeg()
        print(f"   setup_ffmpeg() result: {result}")
        
        # Test pydub after setup
        test_pydub_configuration()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_webm_processing():
    """Test WebM processing specifically"""
    print("\n🎤 Testing WebM Processing (Interview Recording)...")
    
    try:
        from services.audio_processing import process_audio
        
        # Create a mock WebM file
        class MockFile:
            def __init__(self, filename, content=b"fake webm content"):
                self.filename = filename
                self.content = content
            
            def save(self, path):
                with open(path, 'wb') as f:
                    f.write(self.content)
        
        mock_file = MockFile("test_interview.webm")
        
        try:
            result_path, duration = process_audio(mock_file)
            print(f"   ✅ WebM processing succeeded: {result_path}, {duration}s")
            
            # Clean up
            if os.path.exists(result_path):
                os.remove(result_path)
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"   ❌ WebM processing failed: {error_msg}")
            
            # Check if it's the expected FFmpeg error
            if "FFmpeg" in error_msg:
                print("   💡 This is the FFmpeg error we're trying to fix")
            
            return False
            
    except Exception as e:
        print(f"   ❌ WebM test setup failed: {e}")
        return False

def test_direct_ffmpeg_call():
    """Test calling FFmpeg directly"""
    print("\n🔧 Testing Direct FFmpeg Call...")
    
    try:
        import subprocess
        
        # Try to call ffmpeg directly
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ FFmpeg callable from command line")
            version_line = result.stdout.split('\n')[0]
            print(f"   Version: {version_line}")
            return True
        else:
            print(f"   ❌ FFmpeg call failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ❌ FFmpeg call timed out")
        return False
    except FileNotFoundError:
        print("   ❌ FFmpeg not found in PATH")
        return False
    except Exception as e:
        print(f"   ❌ FFmpeg call error: {e}")
        return False

def test_pydub_with_ffmpeg():
    """Test pydub with FFmpeg for a simple operation"""
    print("\n🎵 Testing pydub with FFmpeg...")
    
    try:
        from pydub import AudioSegment
        from pydub.generators import Sine
        
        # Create a simple tone
        tone = Sine(440).to_audio_segment(duration=1000)
        
        # Try to export to different formats
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            wav_path = f.name
        
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            mp3_path = f.name
        
        try:
            # Export to WAV (should work without FFmpeg)
            tone.export(wav_path, format="wav")
            print("   ✅ WAV export works")
            
            # Export to MP3 (requires FFmpeg)
            tone.export(mp3_path, format="mp3")
            print("   ✅ MP3 export works (FFmpeg is working)")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Export failed: {e}")
            return False
            
        finally:
            # Clean up
            for path in [wav_path, mp3_path]:
                if os.path.exists(path):
                    os.remove(path)
            
    except Exception as e:
        print(f"   ❌ pydub test failed: {e}")
        return False

def main():
    """Run comprehensive FFmpeg debugging"""
    print("🔍 FFmpeg Runtime Debug")
    print("=" * 50)
    
    tests = [
        ("Direct FFmpeg Call", test_direct_ffmpeg_call),
        ("Audio Processing Import", test_audio_processing_import),
        ("pydub with FFmpeg", test_pydub_with_ffmpeg),
        ("WebM Processing", test_webm_processing)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running: {test_name}")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Debug Results:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed < len(results):
        print("\n💡 Troubleshooting Suggestions:")
        
        if results[0][1] == False:  # Direct FFmpeg call failed
            print("   - FFmpeg may not be in PATH")
            print("   - Try restarting your terminal/IDE")
            print("   - Verify FFmpeg installation")
        
        if results[1][1] == False:  # Import failed
            print("   - Check Python path and module imports")
            print("   - Verify backend directory structure")
        
        if results[2][1] == False:  # pydub failed
            print("   - pydub may not be finding FFmpeg")
            print("   - Try setting FFMPEG_BINARY environment variable")
        
        if results[3][1] == False:  # WebM failed
            print("   - This is the specific issue affecting interview mode")
            print("   - Focus on fixing pydub FFmpeg configuration")

if __name__ == "__main__":
    main()