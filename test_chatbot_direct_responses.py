#!/usr/bin/env python3
"""
Test direct responses from improved chatbot
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

from services.interview_chatbot import interview_chatbot

def test_direct_responses():
    """Test that chatbot gives direct, helpful answers instead of asking questions back"""
    
    print("🤖 Testing Direct Response Improvements")
    print("=" * 60)
    
    # Test cases that previously might have resulted in questions back
    test_cases = [
        "How do I prepare for an interview?",
        "Give me some tips",
        "I need help with practice", 
        "What should I do?",
        "Can you help me?",
        "I don't know what to say",
        "I'm confused about interviews"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n{i}. User: {question}")
        response = interview_chatbot.get_response(question)
        
        # Check if response is direct (doesn't end with question mark)
        is_direct = not response.strip().endswith('?')
        has_actionable_content = any(word in response.lower() for word in ['here', 'try', 'focus', 'remember', 'practice', 'prepare'])
        
        status = "✅ DIRECT" if is_direct and has_actionable_content else "❌ ASKING QUESTIONS"
        
        print(f"   {status}")
        print(f"   Bot: {response[:200]}{'...' if len(response) > 200 else ''}")
    
    print("\n" + "=" * 60)
    print("✅ Direct response test completed!")

if __name__ == "__main__":
    test_direct_responses()