"""
Demo script to test the AI Public Speaking Feedback System
This script demonstrates the core functionality without the web interface
"""

from app import SpeechAnalyzer
import os

def test_speech_analysis():
    """Test the speech analysis functionality"""
    
    print("🎤 AI Public Speaking Feedback System - Demo Test")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = SpeechAnalyzer()
    
    # Test with sample text (simulating speech-to-text output)
    sample_speeches = [
        {
            'name': 'Fast Speaker',
            'text': 'Hello everyone I am very excited to be here today to talk about artificial intelligence and machine learning these technologies are revolutionizing the way we work and live they are changing everything from healthcare to transportation to education the possibilities are endless and the future is bright',
            'duration': 15  # seconds
        },
        {
            'name': 'Filler Heavy Speaker',
            'text': 'Um hello everyone so like I am uh very excited to be here today you know I want to um talk about like artificial intelligence and uh machine learning so basically these technologies are um really changing everything',
            'duration': 25  # seconds
        },
        {
            'name': 'Confident Speaker',
            'text': 'Good morning everyone I am thrilled to be here today to share my passion for artificial intelligence and machine learning these incredible technologies are transforming our world in amazing ways from revolutionizing healthcare to advancing education AI is creating endless opportunities for innovation and growth',
            'duration': 20  # seconds
        }
    ]
    
    for i, speech in enumerate(sample_speeches, 1):
        print(f"\n📊 Analysis {i}: {speech['name']}")
        print("-" * 30)
        
        # Perform analysis
        speaking_speed = analyzer.calculate_speaking_speed(speech['text'], speech['duration'])
        filler_words, total_fillers = analyzer.analyze_filler_words(speech['text'])
        sentiment_analysis = analyzer.analyze_sentiment(speech['text'])
        
        # Create analysis results
        analysis_results = {
            'transcript': speech['text'],
            'speaking_speed': speaking_speed,
            'filler_words': filler_words,
            'total_filler_words': total_fillers,
            'sentiment': sentiment_analysis
        }
        
        # Generate feedback
        feedback = analyzer.generate_feedback(analysis_results)
        
        # Display results
        print(f"📝 Transcript: {speech['text'][:100]}...")
        print(f"⚡ Speaking Speed: {speaking_speed} WPM")
        print(f"🚫 Filler Words: {total_fillers}")
        print(f"😊 Sentiment: {sentiment_analysis['sentiment']} ({sentiment_analysis['polarity']})")
        print(f"🎯 Confidence Score: {analysis_results.get('confidence_score', 'N/A')}/100")
        
        print("\n💡 Feedback:")
        for j, fb in enumerate(feedback, 1):
            print(f"   {j}. {fb}")
        
        print("\n" + "="*50)

def test_audio_file():
    """Test with actual audio file if available"""
    
    print("\n🎵 Testing with Audio File")
    print("-" * 30)
    
    # Check if test audio files exist
    test_files = ['uploads/confident_speech.wav', 'uploads/fast_speech.wav', 'uploads/filler_heavy.wav']
    
    analyzer = SpeechAnalyzer()
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\n🔍 Analyzing: {file_path}")
            try:
                # Convert audio to text
                transcript = analyzer.audio_to_text(file_path)
                if transcript:
                    print(f"✅ Transcription successful: {transcript[:100]}...")
                else:
                    print("❌ Could not transcribe audio")
            except Exception as e:
                print(f"❌ Error: {e}")
            break
    else:
        print("ℹ️  No test audio files found. Run test_audio_generator.py first or upload your own audio files.")

if __name__ == "__main__":
    # Test text analysis
    test_speech_analysis()
    
    # Test audio file processing
    test_audio_file()
    
    print("\n🎉 Demo completed!")
    print("To run the full web application, execute: python app.py")