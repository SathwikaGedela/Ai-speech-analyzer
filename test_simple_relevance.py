"""
Simple test to verify question relevance analysis works
"""

from backend.services.question_relevance import QuestionRelevanceAnalyzer

def test_simple_cases():
    """Test with simple cases to verify functionality"""
    analyzer = QuestionRelevanceAnalyzer()
    
    print("🧪 Testing Question Relevance Analysis - Simple Cases")
    print("=" * 60)
    
    # Test case 1: Good relevant answer
    question1 = "Tell me about yourself"
    answer1 = "I have experience in software development and my goal is to grow as a leader."
    
    result1 = analyzer.analyze_relevance(question1, answer1)
    print(f"\n📝 Test 1 - Good Answer:")
    print(f"Question: {question1}")
    print(f"Answer: {answer1}")
    print(f"Score: {result1.relevance_score}% ({result1.classification.value})")
    print(f"Type: {result1.question_type.value}")
    print(f"Time: {result1.processing_time:.2f}s")
    
    # Test case 2: Completely off-topic answer
    question2 = "Tell me about yourself"
    answer2 = "I like pizza and the weather is nice."
    
    result2 = analyzer.analyze_relevance(question2, answer2)
    print(f"\n📝 Test 2 - Off-topic Answer:")
    print(f"Question: {question2}")
    print(f"Answer: {answer2}")
    print(f"Score: {result2.relevance_score}% ({result2.classification.value})")
    print(f"Type: {result2.question_type.value}")
    print(f"Time: {result2.processing_time:.2f}s")
    
    # Verify basic functionality
    assert 0 <= result1.relevance_score <= 100
    assert 0 <= result2.relevance_score <= 100
    assert result1.relevance_score > result2.relevance_score  # Good answer should score higher
    
    print(f"\n✅ Basic functionality verified!")
    print(f"Good answer scored {result1.relevance_score}% vs off-topic answer {result2.relevance_score}%")

if __name__ == "__main__":
    test_simple_cases()