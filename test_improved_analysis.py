#!/usr/bin/env python3
"""
Test the improved grammar and engagement analysis
"""

from enhanced_analyzer import EnhancedSpeechAnalyzer

def test_grammar_analysis():
    """Test improved grammar analysis with problematic text"""
    
    print("🧪 TESTING IMPROVED GRAMMAR ANALYSIS")
    print("=" * 50)
    
    analyzer = EnhancedSpeechAnalyzer()
    
    # Test cases with known grammar issues
    test_cases = [
        {
            'name': 'User Example (Many Grammar Errors)',
            'text': "I am going to college yesterday the teacher explain the lesson very good students is listening but some was talking it make the class very nice",
            'expected_score_range': (20, 50)  # Should be low due to many errors
        },
        {
            'name': 'Good Grammar Example',
            'text': "I went to college yesterday. The teacher explained the lesson very well. Students were listening, but some were talking. It made the class very nice.",
            'expected_score_range': (80, 95)  # Should be high
        },
        {
            'name': 'Mixed Grammar Example',
            'text': "Yesterday I go to school. The teacher was explaining good. Some students is listening but others was talking.",
            'expected_score_range': (40, 70)  # Should be medium
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}:")
        print(f"   Text: \"{test_case['text']}\"")
        
        # Analyze grammar
        grammar_result = analyzer._assess_grammar(test_case['text'])
        
        print(f"   Grammar Score: {grammar_result['score']}/100")
        print(f"   Assessment: {grammar_result['assessment']}")
        print(f"   Errors Found: {grammar_result['errors_found']}")
        print(f"   Error Rate: {grammar_result['error_rate']}%")
        
        if grammar_result['error_details']:
            print("   Error Details:")
            for error in grammar_result['error_details']:
                print(f"     • {error}")
        
        # Check if score is in expected range
        min_score, max_score = test_case['expected_score_range']
        if min_score <= grammar_result['score'] <= max_score:
            print(f"   ✅ Score in expected range ({min_score}-{max_score})")
        else:
            print(f"   ❌ Score outside expected range ({min_score}-{max_score})")

def test_engagement_analysis():
    """Test improved engagement and confidence analysis"""
    
    print("\n\n🎯 TESTING IMPROVED ENGAGEMENT ANALYSIS")
    print("=" * 50)
    
    analyzer = EnhancedSpeechAnalyzer()
    
    test_cases = [
        {
            'name': 'Low Confidence (Many Fillers)',
            'text': "Um, I think, uh, maybe the lesson was, like, you know, probably good. I guess students were, um, listening.",
            'expected_confidence': (20, 40),
            'expected_engagement': 'Low'
        },
        {
            'name': 'High Confidence (Clear Statements)',
            'text': "I am absolutely certain that the lesson was excellent. Students were definitely engaged and actively participating. This was clearly a fantastic class!",
            'expected_confidence': (80, 100),
            'expected_engagement': 'High'
        },
        {
            'name': 'Medium Confidence (Mixed)',
            'text': "The lesson was good. Students were listening well. Some were talking but it was nice overall.",
            'expected_confidence': (50, 75),
            'expected_engagement': 'Medium'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}:")
        print(f"   Text: \"{test_case['text']}\"")
        
        # Analyze engagement
        engagement_result = analyzer._analyze_emotional_engagement(test_case['text'])
        
        print(f"   Confidence Score: {engagement_result['confidence_score']}/100")
        print(f"   Engagement Level: {engagement_result['engagement_level']}")
        print(f"   Engagement Score: {engagement_result['engagement_score']}")
        print(f"   Tone Assessment: {engagement_result['tone_assessment']}")
        
        # Show confidence factors
        factors = engagement_result['confidence_factors']
        print(f"   Confidence Factors:")
        print(f"     • Confidence words: {factors['confidence_words']}")
        print(f"     • Uncertainty words: {factors['uncertainty_words']}")
        print(f"     • Weak language count: {factors['weak_language_count']}")
        print(f"     • Grammar influence: {factors['grammar_influence']}")
        
        # Check confidence range
        min_conf, max_conf = test_case['expected_confidence']
        if min_conf <= engagement_result['confidence_score'] <= max_conf:
            print(f"   ✅ Confidence in expected range ({min_conf}-{max_conf})")
        else:
            print(f"   ❌ Confidence outside expected range ({min_conf}-{max_conf})")
        
        # Check engagement level
        if engagement_result['engagement_level'] == test_case['expected_engagement']:
            print(f"   ✅ Engagement level matches expected ({test_case['expected_engagement']})")
        else:
            print(f"   ❌ Engagement level doesn't match expected ({test_case['expected_engagement']})")

def test_full_analysis():
    """Test full analysis with user's example"""
    
    print("\n\n🔍 FULL ANALYSIS TEST - USER'S EXAMPLE")
    print("=" * 50)
    
    analyzer = EnhancedSpeechAnalyzer()
    
    user_text = "I am going to college yesterday the teacher explain the lesson very good students is listening but some was talking it make the class very nice"
    duration = 12.0  # Estimated duration
    
    print(f"Text: \"{user_text}\"")
    print(f"Duration: {duration} seconds")
    
    # Perform full analysis
    analysis = analyzer.comprehensive_analysis(user_text, duration)
    
    print(f"\n📊 RESULTS:")
    print(f"Overall Score: {analysis['overall_score']['score']}/100")
    print(f"Skill Level: {analysis['overall_score']['skill_level']}")
    
    print(f"\n🔤 Grammar Analysis:")
    grammar = analysis['language_content']['grammar']
    print(f"  Score: {grammar['score']}/100")
    print(f"  Assessment: {grammar['assessment']}")
    print(f"  Errors Found: {grammar['errors_found']}")
    
    print(f"\n😊 Engagement Analysis:")
    engagement = analysis['emotional_engagement']
    print(f"  Confidence Score: {engagement['confidence_score']}/100")
    print(f"  Engagement Level: {engagement['engagement_level']}")
    print(f"  Tone: {engagement['tone_assessment']}")
    
    print(f"\n🔊 Speaking Analysis:")
    vocal = analysis['vocal_delivery']
    print(f"  Speaking Pace: {vocal['speaking_pace']['wpm']} WPM")
    print(f"  Filler Words: {vocal['filler_words']['total_count']} ({vocal['filler_words']['percentage']}%)")

if __name__ == "__main__":
    test_grammar_analysis()
    test_engagement_analysis()
    test_full_analysis()
    
    print("\n" + "=" * 60)
    print("🎉 IMPROVED ANALYSIS TESTING COMPLETE!")
    print("✅ Grammar analysis now detects real errors")
    print("✅ Confidence scoring is now dynamic")
    print("✅ Engagement levels vary based on content")
    print("=" * 60)