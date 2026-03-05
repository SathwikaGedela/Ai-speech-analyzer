"""
Test MP3 support directly with the SpeechAnalyzer class
"""

from app import SpeechAnalyzer
import os

def test_mp3_processing():
    print("🎵 Testing MP3 Processing")
    print("=" * 30)
    
    # Check if we have any MP3 files to test with
    test_files = []
    
    # Look for MP3 files in uploads directory
    if os.path.exists('uploads'):
        for file in os.listdir('uploads'):
            if file.lower().endswith('.mp3'):
                test_files.append(os.path.join('uploads', file))
    
    if not test_files:
        print("ℹ️  No MP3 files found in uploads/ directory")
        print("To test MP3 support:")
        print("1. Place an MP3 file in the uploads/ folder")
        print("2. Run this test again")
        print("3. Or use the web interface at http://127.0.0.1:5000")
        return
    
    # Test with the first MP3 file found
    test_file = test_files[0]
    print(f"🔍 Testing with: {test_file}")
    
    try:
        analyzer = SpeechAnalyzer()
        
        print("🎙️  Converting MP3 to text...")
        transcript = analyzer.audio_to_text(test_file)
        
        if transcript:
            print(f"✅ Success! Transcript: {transcript[:100]}...")
            
            # Test other analysis features
            print("📊 Running full analysis...")
            
            # Get duration (approximate)
            from pydub import AudioSegment
            audio_segment = AudioSegment.from_mp3(test_file)
            duration = len(audio_segment) / 1000.0
            
            # Analyze
            wpm = analyzer.calculate_speaking_speed(transcript, duration)
            filler_words, total_fillers = analyzer.analyze_filler_words(transcript)
            sentiment = analyzer.analyze_sentiment(transcript)
            
            print(f"⚡ Speaking Speed: {wpm} WPM")
            print(f"🚫 Filler Words: {total_fillers}")
            print(f"😊 Sentiment: {sentiment['sentiment']} ({sentiment['polarity']})")
            
            print("\n🎉 MP3 support is working perfectly!")
            
        else:
            print("❌ Could not transcribe the audio")
            print("This might be due to:")
            print("- Poor audio quality")
            print("- No speech in the file")
            print("- Network issues with Google Speech API")
            
    except Exception as e:
        print(f"❌ Error processing MP3: {e}")
        print("This might indicate an issue with FFmpeg or pydub")

if __name__ == "__main__":
    test_mp3_processing()