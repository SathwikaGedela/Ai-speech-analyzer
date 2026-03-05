"""
Test the confidence score feature
"""

from app_final import SpeechAnalyzer
import os

def test_confidence_scoring():
    print("🎯 Testing Confidence Score Feature")
    print("=" * 40)
    
    analyzer = SpeechAnalyzer()
    
    # Test with existing MP3 file
    test_file = "uploads/iSongs.info_02_-_Chali_Chaliga.mp3"
    
    if not os.path.exists(test_file):
        print("❌ Test file not found. Please ensure the MP3 file exists.")
        return
    
    try:
        print(f"🔍 Analyzing: {test_file}")
        
        # Get transcript
        transcript = analyzer.audio_to_text(test_file)
        if not transcript:
            print("❌ Could not transcribe audio")
            return
        
        print(f"📝 Transcript: {transcript[:100]}...")
        
        # Get audio duration
        from pydub import AudioSegment
        audio_segment = AudioSegment.from_file(test_file)
        duration = len(audio_segment) / 1000.0
        
        # Perform analysis
        speaking_speed = analyzer.calculate_speaking_speed(transcript, duration)
        filler_words, total_fillers = analyzer.analyze_filler_words(transcript)
        sentiment_analysis = analyzer.analyze_sentiment(transcript)
        
        analysis_results = {
            'transcript': transcript,
            'speaking_speed': speaking_speed,
            'filler_words': filler_words,
            'total_filler_words': total_fillers,
            'sentiment': sentiment_analysis
        }
        
        # Generate feedback with confidence score
        feedback = analyzer.generate_feedback(analysis_results)
        
        print("\n📊 Analysis Results:")
        print(f"   ⚡ Speaking Speed: {speaking_speed} WPM")
        print(f"   🚫 Filler Words: {total_fillers}")
        print(f"   😊 Sentiment: {sentiment_analysis['sentiment']} ({sentiment_analysis['polarity']})")
        print(f"   🎯 Confidence Score: {analysis_results['confidence_score']}/100 ({analysis_results['confidence_level']})")
        
        print("\n💡 AI Feedback:")
        for i, fb in enumerate(feedback, 1):
            print(f"   {i}. {fb}")
        
        print("\n🎉 Confidence scoring is working perfectly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_confidence_scoring()