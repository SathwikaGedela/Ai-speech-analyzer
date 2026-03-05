"""
Test the final app version
"""

from app_final import SpeechAnalyzer
import os

def test_final_app():
    print("🎯 Testing Final App Version")
    print("=" * 30)
    
    analyzer = SpeechAnalyzer()
    
    # Test with existing files
    test_files = []
    
    if os.path.exists('uploads'):
        for file in os.listdir('uploads'):
            if file.lower().endswith(('.wav', '.mp3')):
                test_files.append(os.path.join('uploads', file))
    
    if not test_files:
        print("ℹ️  No audio files found in uploads/ directory")
        print("Please add a WAV or MP3 file to test with.")
        return
    
    for test_file in test_files[:2]:  # Test first 2 files
        print(f"\n🔍 Testing: {test_file}")
        
        try:
            transcript = analyzer.audio_to_text(test_file)
            
            if transcript:
                print(f"✅ Success! Transcript: {transcript[:80]}...")
                
                # Test analysis
                from pydub import AudioSegment
                try:
                    audio_segment = AudioSegment.from_file(test_file)
                    duration = len(audio_segment) / 1000.0
                    
                    wpm = analyzer.calculate_speaking_speed(transcript, duration)
                    filler_words, total_fillers = analyzer.analyze_filler_words(transcript)
                    sentiment = analyzer.analyze_sentiment(transcript)
                    
                    print(f"   ⚡ Speed: {wpm} WPM")
                    print(f"   🚫 Fillers: {total_fillers}")
                    print(f"   😊 Sentiment: {sentiment['sentiment']}")
                    
                except Exception as duration_error:
                    print(f"   ⚠️ Duration calculation failed: {duration_error}")
                    
            else:
                print("❌ Could not transcribe audio")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            if "MP3 processing failed" in str(e):
                print("   💡 Try converting MP3 to WAV format")

if __name__ == "__main__":
    test_final_app()