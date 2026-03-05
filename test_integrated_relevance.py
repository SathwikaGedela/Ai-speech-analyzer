"""
Test the integrated question relevance analysis system
"""

from backend.services.question_relevance import QuestionRelevanceAnalyzer

def test_different_question_types():
    """Test relevance analysis with different question types and answers"""
    analyzer = QuestionRelevanceAnalyzer()
    
    test_cases = [
        {
            "question": "Tell me about yourself",
            "answer": "I have 5 years of experience in software development, specializing in Python and web applications. I'm passionate about creating user-friendly solutions and have led several successful projects. My goal is to continue growing as a technical leader.",
            "expected_type": "personal"
        },
        {
            "question": "Describe a challenging situation you faced at work",
            "answer": "Last year, our team faced a critical deadline with a major client. The situation was challenging because we had limited resources. I took the initiative to reorganize our workflow and coordinate with other teams. As a result, we delivered the project on time and the client was very satisfied.",
            "expected_type": "behavioral"
        },
        {
            "question": "Why should we hire you?",
            "answer": "You should hire me because I bring strong technical skills, proven leadership experience, and a track record of delivering results. I'm particularly good at problem-solving and working with cross-functional teams. I believe I can add significant value to your organization.",
            "expected_type": "value_proposition"
        },
        {
            "question": "Tell me about yourself",
            "answer": "I like pizza and watching movies. The weather is nice today. I have a dog named Max.",
            "expected_type": "personal"
        }
    ]
    
    print("🧪 Testing Question Relevance Analysis System")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Question: {test_case['question']}")
        print(f"Answer: {test_case['answer']}")
        
        result = analyzer.analyze_relevance(test_case['question'], test_case['answer'])
        
        print(f"\n📊 Results:")
        print(f"  Relevance Score: {result.relevance_score}%")
        print(f"  Classification: {result.classification.value}")
        print(f"  Question Type: {result.question_type.value}")
        print(f"  Processing Time: {result.processing_time:.2f}s")
        print(f"  Topic Overlap: {result.topic_overlap.overlap_percentage:.1f}%")
        
        print(f"\n💬 Feedback:")
        print(f"  Summary: {result.feedback.summary}")
        if result.feedback.strengths:
            print(f"  Strengths: {', '.join(result.feedback.strengths)}")
        if result.feedback.improvements:
            print(f"  Improvements: {', '.join(result.feedback.improvements)}")
        if result.feedback.specific_suggestions:
            print(f"  Suggestions: {', '.join(result.feedback.specific_suggestions)}")
        
        # Validate basic properties
        assert 0 <= result.relevance_score <= 100, f"Invalid relevance score: {result.relevance_score}"
        assert result.processing_time < 3.0, f"Processing too slow: {result.processing_time}s"
        assert result.question_type.value == test_case['expected_type'], f"Wrong question type: expected {test_case['expected_type']}, got {result.question_type.value}"
        
        print(f"  ✅ Test case {i} passed!")
        print("-" * 60)
    
    print(f"\n🎉 All test cases completed successfully!")
    print("The Question Relevance Analysis system is working correctly.")

if __name__ == "__main__":
    test_different_question_types()