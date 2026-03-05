#!/usr/bin/env python3
"""
Test Expanded Knowledge Base
"""

import sys
import os
sys.path.append('backend')

from services.universal_chatbot import universal_chatbot

def test_expanded_knowledge():
    """Test the expanded knowledge base"""
    
    print("🎯 TESTING EXPANDED KNOWLEDGE BASE")
    print("=" * 60)
    
    # Test the newly added topics
    test_questions = [
        "What is DBMS?",
        "What are variables?", 
        "What is 5G?",
        "What is virtual reality?",
        "What is Internet of Things?",
        "What is cybersecurity?",
        "What is big data?",
        "What is blockchain?",
        "What is cryptocurrency?",
        "What is gravity?",
        "What is DNA?",
        "Explain photosynthesis",
        "What are neural networks?"
    ]
    
    perfect_count = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"📝 Test {i}")
        print(f"Question: {question}")
        print("-" * 40)
        
        try:
            response = universal_chatbot.get_response(question)
            
            # Check if we got a comprehensive response
            if len(response) > 500 and ('**' in response or '•' in response):
                print(f"✅ PERFECT - Comprehensive explanation!")
                perfect_count += 1
            elif len(response) > 200:
                print(f"👍 GOOD - Detailed response")
            else:
                print(f"⚠️  BASIC - Could be more detailed")
            
            print(f"Response: {response[:150]}...")
            print(f"Length: {len(response)} characters")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*40 + "\n")
    
    print(f"🎉 RESULTS: {perfect_count}/{len(test_questions)} perfect answers ({perfect_count/len(test_questions)*100:.1f}%)")

if __name__ == "__main__":
    test_expanded_knowledge()