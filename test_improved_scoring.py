"""
Test the improved relevance scoring with the user's actual answer
"""

from backend.services.question_relevance_simple import QuestionRelevanceAnalyzer

def test_user_answer():
    """Test with the user's actual answer"""
    analyzer = QuestionRelevanceAnalyzer()
    
    question = "Why should we hire you?"
    answer = "you should hire me because I am a quick learner with strong willingness to grow and adapt I have a positive attitude the problem solving skills and the ability to work well both independently and in a team I am committed to delivering quality work and continuously improving my skills I'll bring dedication responsibility and enthusiasm to this role"
    
    print("🧪 Testing Improved Relevance Scoring")
    print("=" * 60)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print()
    
    result = analyzer.analyze_relevance(question, answer)
    
    print("📊 IMPROVED RESULTS:")
    print(f"   Relevance Score: {result.relevance_score}%")
    print(f"   Classification: {result.classification.value}")
    print(f"   Question Type: {result.question_type.value}")
    print()
    
    print("💡 FEEDBACK:")
    print(f"   Summary: {result.feedback.summary}")
    
    if result.feedback.strengths:
        print(f"   ✅ Strengths:")
        for strength in result.feedback.strengths:
            print(f"      • {strength}")
    
    if result.feedback.improvements:
        print(f"   🔧 Improvements:")
        for improvement in result.feedback.improvements:
            print(f"      • {improvement}")
    
    if result.feedback.specific_suggestions:
        print(f"   💡 Suggestions:")
        for suggestion in result.feedback.specific_suggestions:
            print(f"      • {suggestion}")
    
    print()
    print("🎯 ANALYSIS:")
    print("This answer should score much higher because it:")
    print("✅ Directly answers 'Why should we hire you?'")
    print("✅ Mentions relevant skills and qualities")
    print("✅ Shows value proposition (dedication, responsibility)")
    print("✅ Demonstrates understanding of the question")
    print("✅ Provides substantial content (40+ words)")

if __name__ == "__main__":
    test_user_answer()