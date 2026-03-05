"""
Interview Questions Bank
Simple, editable, and extendable question database
"""

INTERVIEW_QUESTIONS = {
    "hr": [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?",
        "Why should we hire you?",
        "Where do you see yourself in five years?",
        "Why are you leaving your current job?",
        "What motivates you?",
        "How do you handle stress and pressure?",
        "What are your salary expectations?"
    ],
    "technical": [
        "Explain a project you worked on.",
        "What is overfitting in machine learning?",
        "Explain REST APIs.",
        "What challenges did you face in your last project?",
        "How do you debug code?",
        "Explain the difference between SQL and NoSQL databases.",
        "What is version control and why is it important?",
        "How do you ensure code quality?"
    ],
    "behavioral": [
        "Describe a challenging situation and how you handled it.",
        "Tell me about a failure and what you learned.",
        "How do you handle deadlines?",
        "Give an example of when you had to work with a difficult team member.",
        "Describe a time when you had to learn something new quickly.",
        "Tell me about a time you disagreed with your manager.",
        "How do you prioritize your work?",
        "Describe a time when you went above and beyond."
    ]
}

def get_questions_by_category(category):
    """Get questions for a specific category"""
    return INTERVIEW_QUESTIONS.get(category, [])

def get_all_categories():
    """Get all available interview categories"""
    return list(INTERVIEW_QUESTIONS.keys())

def get_random_question(category=None):
    """Get a random question from a category or all categories"""
    import random
    
    if category and category in INTERVIEW_QUESTIONS:
        return random.choice(INTERVIEW_QUESTIONS[category])
    
    # Get random question from all categories
    all_questions = []
    for questions in INTERVIEW_QUESTIONS.values():
        all_questions.extend(questions)
    
    return random.choice(all_questions) if all_questions else None