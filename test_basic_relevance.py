"""
Basic test to verify question relevance analysis infrastructure works
"""

from backend.services.question_relevance import QuestionRelevanceAnalyzer

def test_basic_functionality():
    """Test that the basic relevance analysis works"""
    analyzer = QuestionRelevanceAnalyzer()
    
    # Test with a simple question-answer pair
    question = "Tell me about yourself"
    answer = "I have 5 years of experience in software development and I'm passionate about creating innovative solutions."
    
    result = analyzer.analyze_relevance(question, answer)
    
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print(f"Relevance Score: {result.relevance_score}%")
    print(f"Classification: {result.classification.value}")
    print(f"Question Type: {result.question_type.value}")
    print(f"Processing Time: {result.processing_time:.2f}s")
    print(f"Feedback Summary: {result.feedback.summary}")
    
    # Basic assertions
    assert 0 <= result.relevance_score <= 100
    assert result.processing_time < 3.0
    assert result.feedback.summary
    
    print("✅ Basic functionality test passed!")

if __name__ == "__main__":
    test_basic_functionality()