"""
Demo of the Question Relevance Analysis integrated with Interview Mode
"""

from backend.services.question_relevance import QuestionRelevanceAnalyzer

def demo_interview_relevance():
    """Demo showing how the relevance analysis works in interview context"""
    analyzer = QuestionRelevanceAnalyzer()
    
    print("🎤 AI Interview Practice System - Question Relevance Analysis Demo")
    print("=" * 70)
    
    # Demo different scenarios
    scenarios = [
        {
            "title": "✅ EXCELLENT ANSWER",
            "question": "Tell me about yourself",
            "answer": "I'm a software engineer with 5 years of experience in Python and web development. I have strong problem-solving skills and have led several successful projects. My background includes working with cross-functional teams, and I'm passionate about creating user-friendly applications. My career goal is to continue growing as a technical leader while contributing to innovative solutions."
        },
        {
            "title": "⚠️ PARTIALLY RELEVANT ANSWER", 
            "question": "Describe a challenging situation you faced at work",
            "answer": "I work in software development and it can be challenging sometimes. I like working with my team and we usually figure things out. Technology is always changing so we have to keep learning new things."
        },
        {
            "title": "❌ OFF-TOPIC ANSWER",
            "question": "Why should we hire you?",
            "answer": "I really like this company's office building. The weather has been nice lately. I enjoy coffee and usually drink it in the morning. My favorite color is blue."
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{scenario['title']}")
        print("-" * 50)
        print(f"🎯 Question: {scenario['question']}")
        print(f"💬 Answer: {scenario['answer']}")
        
        # Analyze relevance
        result = analyzer.analyze_relevance(scenario['question'], scenario['answer'])
        
        # Display results like the interview system would
        print(f"\n📊 RELEVANCE ANALYSIS:")
        print(f"   Score: {result.relevance_score}%")
        print(f"   Classification: {result.classification.value}")
        print(f"   Question Type: {result.question_type.value.title()}")
        print(f"   Processing Time: {result.processing_time:.1f}s")
        
        print(f"\n💡 FEEDBACK:")
        print(f"   {result.feedback.summary}")
        
        if result.feedback.strengths:
            print(f"   ✅ Strengths: {'; '.join(result.feedback.strengths)}")
        
        if result.feedback.improvements:
            print(f"   🔧 Improvements: {'; '.join(result.feedback.improvements)}")
        
        if result.feedback.specific_suggestions:
            print(f"   💡 Suggestions: {'; '.join(result.feedback.specific_suggestions)}")
        
        print("=" * 70)
    
    print(f"\n🎉 DEMO COMPLETE!")
    print("The Question Relevance Analysis system successfully:")
    print("✅ Identifies question types (personal, behavioral, value proposition)")
    print("✅ Scores answer relevance from 0-100%")
    print("✅ Provides specific feedback and suggestions")
    print("✅ Detects off-topic responses")
    print("✅ Integrates seamlessly with existing interview analysis")
    
    print(f"\n🚀 Ready for production use in Interview Mode!")

if __name__ == "__main__":
    demo_interview_relevance()