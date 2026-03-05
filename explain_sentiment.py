"""
Explain sentiment analysis with clear examples
"""

from textblob import TextBlob

def analyze_sentiment_examples():
    print("🧠 Sentiment Analysis Explained")
    print("=" * 35)
    
    examples = [
        {
            'text': 'I am excited to present our amazing new technology!',
            'description': 'Very positive words'
        },
        {
            'text': 'Good morning everyone. I am here to discuss artificial intelligence.',
            'description': 'Neutral, professional tone'
        },
        {
            'text': 'Um, I am not sure if this will work. It might be difficult.',
            'description': 'Uncertain, negative words'
        },
        {
            'text': 'This is terrible. I hate giving presentations.',
            'description': 'Very negative words'
        },
        {
            'text': 'Thank you for this wonderful opportunity to share my passion!',
            'description': 'Enthusiastic, positive'
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n📝 Example {i}: {example['description']}")
        print(f"Text: \"{example['text']}\"")
        
        # Analyze sentiment
        blob = TextBlob(example['text'])
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment category
        if polarity > 0.1:
            sentiment = "Positive"
            emoji = "😊"
        elif polarity < -0.1:
            sentiment = "Negative"
            emoji = "😐"
        else:
            sentiment = "Neutral"
            emoji = "😑"
        
        print(f"Result: {emoji} {sentiment} (Polarity: {polarity:.3f})")
        
        # Explain what this means
        if polarity > 0.5:
            print("   → Very confident and enthusiastic!")
        elif polarity > 0.1:
            print("   → Positive and engaging tone")
        elif polarity > -0.1:
            print("   → Professional, neutral tone")
        elif polarity > -0.5:
            print("   → Somewhat uncertain or negative")
        else:
            print("   → Very negative or pessimistic")
        
        print("-" * 50)

def explain_why_sentiment_matters():
    print("\n🎯 Why Sentiment Analysis Matters for Public Speaking:")
    print("-" * 55)
    
    reasons = [
        "🔥 **Confidence Detection**: Positive words indicate confidence",
        "👥 **Audience Engagement**: Positive tone keeps audience interested", 
        "😰 **Nervousness Detection**: Negative words may show anxiety",
        "📈 **Improvement Tracking**: Monitor emotional progress over time",
        "🎭 **Tone Awareness**: Help speakers understand how they sound"
    ]
    
    for reason in reasons:
        print(f"• {reason}")
    
    print("\n💡 **In Your System:**")
    print("• Positive sentiment (+0.1 to +1.0) = Confident speaker")
    print("• Neutral sentiment (-0.1 to +0.1) = Professional tone")  
    print("• Negative sentiment (-1.0 to -0.1) = May need encouragement")

if __name__ == "__main__":
    analyze_sentiment_examples()
    explain_why_sentiment_matters()
    
    print("\n🌐 Your system analyzes sentiment automatically!")
    print("📊 It shows up in your web interface as: Sentiment: Positive (0.122)")
    print("🎯 And it affects your confidence score calculation!")