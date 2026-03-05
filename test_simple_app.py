"""
Test the simple app version with MP3 support
"""

from app_simple import SpeechAnalyzer
import os

def test_mp3_with_simple_app():
    print("🎵 Testing Simple App MP3 Support")
    print("=" * 35)
    
    # Look for MP3 files
    mp3_files = []
    if os.path.exists('uploads'):
        for file in os.listdir('uploads'):
            if file.lower().endswith('.mp3'):
                mp3_files.append(os.path.join('uploads', file))
    
    if not mp3_files:
        print("ℹ️  No MP3 files found in uploads/ directory")
        print("Please add an MP3 file to test with.")
        return
    
    # Test with first MP3 file
    test_file = mp3_files[0]
    print(f"🔍 Testing with: {test_file}")
    
    try:
        analyzer = SpeechAnalyzer()
        
        print("🎙️  Converting MP3 to text...")
        transcript = analyzer.audio_to_text(test_file)
        
        if transcript:
            print(f"✅ Success! Transcript: {transcript[:100]}...")
            print("🎉 MP3 support is working with the simple app!")
        else:
            print("❌ Could not transcribe the audio")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        if "MP3 processing failed" in str(e):
            print("\n💡 Suggestion: Try converting your MP3 to WAV format")
            print("   Use: https://cloudconvert.com/mp3-to-wav")

if __name__ == "__main__":
    test_mp3_with_simple_app()