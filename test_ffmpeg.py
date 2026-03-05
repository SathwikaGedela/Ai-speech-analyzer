"""
Test script to check if FFmpeg is working with pydub
"""

def test_ffmpeg():
    print("🔧 Testing FFmpeg installation...")
    
    try:
        from pydub import AudioSegment
        from pydub.utils import which
        
        # Check if FFmpeg is available
        ffmpeg_path = which("ffmpeg")
        if ffmpeg_path:
            print(f"✅ FFmpeg found at: {ffmpeg_path}")
        else:
            print("❌ FFmpeg not found in PATH")
            return False
        
        # Test basic functionality
        print("🧪 Testing pydub with FFmpeg...")
        
        # Create a simple test audio segment
        test_audio = AudioSegment.silent(duration=1000)  # 1 second of silence
        print("✅ pydub is working correctly!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install pydub: pip install pydub")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mp3_support():
    print("\n🎵 Testing MP3 support...")
    
    try:
        from pydub import AudioSegment
        
        # Try to create an MP3 segment (this will test MP3 codec support)
        test_audio = AudioSegment.silent(duration=1000)
        
        # Test export to MP3 format
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
            test_audio.export(temp_file.name, format="mp3")
            print("✅ MP3 support is working!")
            return True
            
    except Exception as e:
        print(f"❌ MP3 support error: {e}")
        print("This might be due to missing codecs or FFmpeg not being in PATH")
        return False

if __name__ == "__main__":
    print("🚀 FFmpeg and Audio Processing Test")
    print("=" * 40)
    
    ffmpeg_ok = test_ffmpeg()
    mp3_ok = test_mp3_support()
    
    print("\n" + "=" * 40)
    if ffmpeg_ok and mp3_ok:
        print("🎉 All tests passed! Your system is ready for MP3 processing.")
        print("You can now use MP3 files with the speech feedback system.")
    else:
        print("⚠️  Some tests failed. You may need to:")
        print("1. Restart your command prompt/terminal")
        print("2. Restart your IDE (VS Code, etc.)")
        print("3. Check if FFmpeg is in your system PATH")
        print("4. Try converting MP3 to WAV as an alternative")