"""
Comprehensive test for all interview question types
Shows how the relevance analysis works for different question categories
"""

from backend.services.question_relevance_simple import QuestionRelevanceAnalyzer

def test_all_question_types():
    """Test relevance analysis for all supported question types"""
    analyzer = QuestionRelevanceAnalyzer()
    
    print("🧪 COMPREHENSIVE QUESTION TYPE TESTING")
    print("=" * 70)
    print("Testing all supported interview question types with good and poor answers")
    print()
    
    test_cases = [
        {
            "category": "1. PERSONAL QUESTIONS",
            "question": "Tell me about yourself",
            "good_answer": "I'm a software engineer with 5 years of experience in web development. I have strong problem-solving skills and enjoy working in collaborative teams. My background includes leading several successful projects, and my career goal is to continue growing as a technical leader while contributing to innovative solutions.",
            "poor_answer": "I like pizza and watching movies. The weather has been nice lately. I have a dog named Max and my favorite color is blue."
        },
        {
            "category": "2. BEHAVIORAL QUESTIONS", 
            "question": "Describe a challenging situation you faced at work",
            "good_answer": "Last year, our team faced a critical deadline with a major client project. The situation was challenging because we had limited resources and tight timeline. I took the initiative to reorganize our workflow, coordinated with other teams, and worked extra hours. As a result, we delivered the project on time and the client was very satisfied with the quality.",
            "poor_answer": "I work in software development and sometimes it's challenging. I usually work with my team and we figure things out. Technology changes a lot."
        },
        {
            "category": "3. VALUE PROPOSITION QUESTIONS",
            "question": "Why should we hire you?",
            "good_answer": "You should hire me because I bring a unique combination of technical skills and leadership experience. I have 5 years of proven experience in software development, strong problem-solving abilities, and a track record of delivering quality results. I'm committed to continuous learning and can contribute immediately to your team's success.",
            "poor_answer": "I really need this job and I think your company is nice. I like the office building and the location is convenient for me."
        },
        {
            "category": "4. STRENGTHS & WEAKNESSES QUESTIONS",
            "question": "What are your greatest strengths and weaknesses?",
            "good_answer": "My greatest strength is my analytical problem-solving ability - I can break down complex issues and find effective solutions. My weakness used to be public speaking, but I've been actively working on it by joining a speaking club and volunteering for presentations. I've seen significant improvement in my confidence.",
            "poor_answer": "I'm good at everything and I don't really have any weaknesses. I'm perfect for any job and never make mistakes."
        },
        {
            "category": "5. TECHNICAL QUESTIONS",
            "question": "How would you design a scalable web application?",
            "good_answer": "I would start by analyzing the requirements and expected load. For scalability, I'd implement a microservices architecture with load balancing, use caching strategies like Redis, design a robust database schema with proper indexing, and implement monitoring systems. I'd also consider cloud services for auto-scaling capabilities.",
            "poor_answer": "I would just make it work and use whatever technology is available. Programming is programming, it doesn't matter which approach you use."
        },
        {
            "category": "6. SITUATIONAL QUESTIONS",
            "question": "What would you do if you disagreed with your manager's decision?",
            "good_answer": "I would first try to understand their perspective by asking clarifying questions. If I still had concerns, I'd respectfully present my viewpoint with supporting data or examples. I'd focus on the business impact and suggest alternative approaches. Ultimately, I'd support the final decision while documenting any risks I identified.",
            "poor_answer": "I would just do whatever they say because they're the boss. I never disagree with authority figures."
        }
    ]
    
    for test_case in test_cases:
        print(f"📋 {test_case['category']}")
        print("-" * 50)
        print(f"🎯 Question: {test_case['question']}")
        print()
        
        # Test good answer
        good_result = analyzer.analyze_relevance(test_case['question'], test_case['good_answer'])
        print("✅ GOOD ANSWER:")
        print(f"   Answer: {test_case['good_answer'][:100]}...")
        print(f"   Score: {good_result.relevance_score}% ({good_result.classification.value})")
        print(f"   Type: {good_result.question_type.value}")
        if good_result.feedback.strengths:
            print(f"   Strengths: {'; '.join(good_result.feedback.strengths[:2])}")
        print()
        
        # Test poor answer
        poor_result = analyzer.analyze_relevance(test_case['question'], test_case['poor_answer'])
        print("❌ POOR ANSWER:")
        print(f"   Answer: {test_case['poor_answer'][:100]}...")
        print(f"   Score: {poor_result.relevance_score}% ({poor_result.classification.value})")
        print(f"   Type: {poor_result.question_type.value}")
        if poor_result.feedback.improvements:
            print(f"   Improvements: {'; '.join(poor_result.feedback.improvements[:2])}")
        print()
        
        print("=" * 70)
        print()
    
    print("🎯 SUMMARY OF QUESTION TYPE SUPPORT:")
    print("✅ Personal Questions - Looks for: experience, background, skills, goals")
    print("✅ Behavioral Questions - Looks for: situation, challenge, action, result (STAR method)")
    print("✅ Value Proposition - Looks for: skills, value, contribute, achievements")
    print("✅ Strengths/Weaknesses - Looks for: strength, weakness, improvement plans")
    print("✅ Technical Questions - Looks for: technical concepts, implementation, design")
    print("✅ Situational Questions - Looks for: approach, strategy, reasoning")
    print()
    print("🤖 SYSTEM DESIGN:")
    print("• Rule-based pattern matching (not ML training)")
    print("• Keyword recognition with related term matching")
    print("• Question-specific scoring algorithms")
    print("• Contextual feedback generation")
    print("• Real-time analysis (no training required)")

def test_off_topic_detection():
    """Test how well the system detects off-topic answers"""
    analyzer = QuestionRelevanceAnalyzer()
    
    print("\n" + "="*70)
    print("🔍 OFF-TOPIC DETECTION TEST")
    print("="*70)
    
    question = "Tell me about your work experience"
    off_topic_answers = [
        "I love pizza and ice cream. My favorite movie is Star Wars. I have three cats.",
        "The weather is really nice today. I went shopping yesterday and bought new shoes.",
        "I enjoy playing video games and listening to music. My hobby is collecting stamps."
    ]
    
    for i, answer in enumerate(off_topic_answers, 1):
        result = analyzer.analyze_relevance(question, answer)
        print(f"Test {i}: {answer}")
        print(f"Score: {result.relevance_score}% ({result.classification.value})")
        print(f"Feedback: {result.feedback.summary}")
        print()

if __name__ == "__main__":
    test_all_question_types()
    test_off_topic_detection()