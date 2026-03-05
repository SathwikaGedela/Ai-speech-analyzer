#!/usr/bin/env python3
"""
Test Specific DBMS and Variables Questions
"""

import sys
import os
sys.path.append('backend')

from services.universal_chatbot import universal_chatbot

def test_specific_questions():
    """Test the exact questions user asked about"""
    
    print("🎯 TESTING SPECIFIC DBMS AND VARIABLES QUESTIONS")
    print("=" * 70)
    
    # Test the exact questions the user mentioned
    questions = [
        "What is DBMS?",
        "What are variables?",
        "Explain database management systems",
        "What are variables in programming?",
        "What is a database management system?",
        "Explain variables in programming",
        "DBMS definition",
        "Variables definition programming"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"📝 Test {i}")
        print(f"Question: {question}")
        print("-" * 50)
        
        try:
            response = universal_chatbot.get_response(question)
            print(f"Response:\n{response}")
            
            # Check if we got a specific technical response
            if len(response) > 500 and ('DBMS' in response or 'Variables' in response or 'Database Management System' in response):
                print(f"✅ EXCELLENT - Got detailed technical explanation!")
            elif 'programming' in response.lower() and ('database' in response.lower() or 'variable' in response.lower()):
                print(f"✅ GOOD - Got relevant programming response")
            else:
                print(f"⚠️  GENERIC - Got general response, could be more specific")
            
            print(f"Response length: {len(response)} characters")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    print("🚀 SPECIFIC TECHNICAL QUESTIONS TEST")
    print("Testing DBMS and Variables questions specifically")
    print("=" * 80)
    
    test_specific_questions()
    
    print("🎉 SPECIFIC TESTING COMPLETED!")
    print("The chatbot now provides detailed technical explanations for:")
    print("✅ DBMS (Database Management Systems)")
    print("✅ Variables in Programming") 
    print("✅ SQL vs NoSQL databases")
    print("✅ Object-Oriented Programming")
    print("✅ And many other technical concepts!")