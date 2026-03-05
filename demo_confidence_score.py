"""
Demo the confidence score feature with sample speech data
"""

from app_final import SpeechAnalyzer

def demo_confidence_scoring():
    print("🎯 AI Public Speaking Feedback - Confidence Score Demo")
    print("=" * 55)
    
    analyzer = SpeechAnalyzer()
    
    # Sample speech scenarios for demonstration
    test_scenarios = [
        {
            'name': 'Confident Speaker',
            'transcript': 'Good morning everyone. I am excited to present our new artificial intelligence system. This technology will revolutionize how we analyze speech patterns and provide valuable feedback to users.',
            'duration': 15,  # seconds
            'description': 'Clear, positive speech with good pace'
        },
        {
            'name': 'Nervous Speaker',
            'transcript': 'Um, hello everyone. So, like, I am, uh, here to talk about, um, artificial intelligence. You know, it is, uh, really complicated and, like, I am not sure if, um, you will understand it.',
            'duration': 20,  # seconds
            'description': 'Many filler words, uncertain tone'
        },
        {
            'name': 'Fast Speaker',
            'transcript': 'Hello everyone I am very excited to be here today to talk about artificial intelligence and machine learning these technologies are revolutionizing everything from healthcare to education and the possibilities are endless.',
            'duration': 8,  # seconds (very fast)
            'description': 'Speaking too fast, hard to follow'
        },
        {
            'name': 'Slow Speaker',
            'transcript': 'Hello... everyone. I am... very excited... to be here... today.',
            'duration': 25,  # seconds (very slow)
            'description': 'Speaking too slowly, may lose audience attention'
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📊 Scenario {i}: {scenario['name']}")
        print(f"📝 Description: {scenario['description']}")
        print("-" * 50)
        
        # Perform analysis
        speaking_speed = analyzer.calculate_speaking_speed(scenario['transcript'], scenario['duration'])
        filler_words, total_fillers = analyzer.analyze_filler_words(scenario['transcript'])
        sentiment_analysis = analyzer.analyze_sentiment(scenario['transcript'])
        
        analysis_results = {
            'transcript': scenario['transcript'],
            'speaking_speed': speaking_speed,
            'filler_words': filler_words,
            'total_filler_words': total_fillers,
            'sentiment': sentiment_analysis
        }
        
        # Generate feedback with confidence score
        feedback = analyzer.generate_feedback(analysis_results)
        
        # Display results
        print(f"⚡ Speaking Speed: {speaking_speed} WPM")
        print(f"🚫 Filler Words: {total_fillers}")
        print(f"😊 Sentiment: {sentiment_analysis['sentiment']} ({sentiment_analysis['polarity']})")
        print(f"🎯 Confidence Score: {analysis_results['confidence_score']}/100 ({analysis_results['confidence_level']})")
        
        print("\n💡 AI Feedback:")
        for j, fb in enumerate(feedback[:3], 1):  # Show first 3 feedback items
            print(f"   {j}. {fb}")
        
        if len(feedback) > 3:
            print(f"   ... and {len(feedback) - 3} more feedback items")
        
        print("\n" + "=" * 55)

def show_confidence_scoring_explanation():
    print("\n🧠 How Confidence Scoring Works:")
    print("-" * 35)
    print("The AI calculates confidence based on:")
    print("• Speaking Speed (optimal: 120-160 WPM)")
    print("• Filler Word Usage (lower is better)")
    print("• Sentiment Analysis (positive tone preferred)")
    print("• Speech Length (not too short or too long)")
    print("\nScore Ranges:")
    print("• 85-100: Excellent confidence")
    print("• 70-84:  Good confidence")
    print("• 55-69:  Fair confidence")
    print("• 40-54:  Needs improvement")
    print("• 0-39:   Poor confidence")

if __name__ == "__main__":
    demo_confidence_scoring()
    show_confidence_scoring_explanation()
    
    print("\n🌐 Your web application is running at: http://127.0.0.1:5000")
    print("🎤 Upload an audio file to test the confidence scoring feature!")
    print("✨ The confidence score will now appear in your analysis results!")