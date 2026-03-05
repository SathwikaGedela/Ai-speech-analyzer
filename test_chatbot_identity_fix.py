#!/usr/bin/env python3
"""
Test the chatbot's responses to personal/identity questions
"""

import sys
import os
sys.path.append('backend')

from services.universal_chatbot import universal_chatbot
from services.comprehensive_knowledge_base import comprehensive_kb

def test_identity_questions():
    """Test various identity and personal questions"""
    
    test_questions = [
        "what is your name",
        "what are you",
        "who are you", 
        "introduce yourself",
        "what can you do",
        "what are your capabilities",
        "are you human",
        "are you ai",
        "are you a robot",
        "how can you help"
    ]
    
    print("=== TESTING CHATBOT IDENTITY RESPONSES ===\n")
    
    for question in test_questions:
        print(f"Question: {question}")
        print("-" * 50)
        
        # Test comprehensive knowledge base first
        kb_response = comprehensive_kb.get_response(question)
        if kb_response:
            print("✅ Knowledge Base Response:")
            print(kb_response[:200] + "..." if len(kb_response) > 200 else kb_response)
        else:
            print("❌ No Knowledge Base Response")
        
        print()
        
        # Test universal chatbot
        chatbot_response = universal_chatbot.get_response(question)
        print("🤖 Universal Chatbot Response:")
        print(chatbot_response[:200] + "..." if len(chatbot_response) > 200 else chatbot_response)
        
        print("\n" + "="*80 + "\n")

def test_technical_questions():
    """Test some technical questions to ensure they still work"""
    
    technical_questions = [
        "what is dbms",
        "what are variables",
        "what is machine learning",
        "explain algorithms"
    ]
    
    print("=== TESTING TECHNICAL QUESTIONS ===\n")
    
    for question in technical_questions:
        print(f"Question: {question}")
        print("-" * 50)
        
        response = universal_chatbot.get_response(question)
        print("Response:")
        print(response[:200] + "..." if len(response) > 200 else response)
        
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    test_identity_questions()
    test_technical_questions()