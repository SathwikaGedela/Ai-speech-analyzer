#!/usr/bin/env python3
"""
Test comprehensive interview question responses
"""

import sys
import os
sys.path.append('backend')

from services.universal_chatbot import universal_chatbot

def test_interview_questions():
    """Test various interview questions"""
    
    interview_questions = [
        "tell me about yourself",
        "tell me about your background", 
        "why should we hire you",
        "what are your strengths",
        "what is your biggest weakness",
        "why do you want to work here",
        "where do you see yourself in 5 years"
    ]
    
    print("=== TESTING INTERVIEW QUESTIONS ===\n")
    
    for question in interview_questions:
        print(f"Question: '{question}'")
        print("-" * 60)
        
        response = universal_chatbot.get_response(question)
        
        # Check if it's a generic response
        is_generic = "I'd be happy to help you with that! While I may not have caught" in response
        
        if is_generic:
            print("❌ Generic response")
        else:
            print("✅ Specific interview guidance:")
            print(response[:250] + "..." if len(response) > 250 else response)
        
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_interview_questions()