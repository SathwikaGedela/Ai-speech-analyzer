#!/usr/bin/env python3
"""
Debug Chatbot Response Issue
"""

import sys
import os
sys.path.append('backend')

from services.universal_chatbot import universal_chatbot

def debug_response_issue():
    """Debug why the chatbot is giving generic responses"""
    
    print("🔍 DEBUGGING CHATBOT RESPONSE ISSUE")
    print("=" * 60)
    
    # Test the response you received
    generic_response = "I believe my combination of technical expertise, problem-solving skills, and collaborative approach makes me well-suited for this role. I'm committed to delivering high-quality work while contributing positively to team goals and driving successful outcomes."
    
    print("You received this generic response:")
    print(f"'{generic_response}'")
    print()
    
    # This looks like a default interview response, let's test some questions
    test_questions = [
        "What is DBMS?",
        "What are variables?", 
        "Tell me about yourself",
        "What are your strengths?",
        "Why should we hire you?",
        "What makes you suitable for this role?",
        "Hello",
        "Help me",
        "Can you explain something?"
    ]
    
    print("Testing various questions to see which ones trigger this response:")
    print("-" * 60)
    
    for question in test_questions:
        print(f"Q: {question}")
        try:
            response = universal_chatbot.get_response(question)
            if generic_response in response or "technical expertise, problem-solving skills" in response:
                print(f"✅ FOUND IT! This question triggers the generic response")
            else:
                print(f"Response: {response[:100]}...")
        except Exception as e:
            print(f"Error: {e}")
        print()

if __name__ == "__main__":
    debug_response_issue()