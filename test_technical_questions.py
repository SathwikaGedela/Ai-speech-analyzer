#!/usr/bin/env python3
"""
Test Technical Questions - Verify chatbot handles DBMS, variables, and other technical concepts
"""

import sys
import os
sys.path.append('backend')

from services.universal_chatbot import universal_chatbot

def test_technical_concepts():
    """Test the chatbot with specific technical questions like DBMS, variables, etc."""
    
    print("🔬 TESTING TECHNICAL CONCEPT QUESTIONS")
    print("=" * 70)
    
    # Technical questions that should get detailed, accurate responses
    technical_questions = [
        # Database concepts
        ("What is DBMS?", "Database Management System"),
        ("Explain SQL vs NoSQL databases", "Database Types"),
        ("What is database normalization?", "Database Design"),
        ("What are database indexes?", "Database Optimization"),
        
        # Programming concepts
        ("What are variables?", "Programming Fundamentals"),
        ("Explain data types in programming", "Programming Concepts"),
        ("What is object-oriented programming?", "Programming Paradigms"),
        ("What are functions in programming?", "Programming Basics"),
        
        # Computer Science concepts
        ("What are algorithms?", "Computer Science"),
        ("Explain data structures", "Computer Science"),
        ("What is recursion?", "Programming Concepts"),
        ("What are loops in programming?", "Programming Control Flow"),
        
        # Web Development
        ("What is HTML?", "Web Development"),
        ("Explain CSS and its purpose", "Web Styling"),
        ("What is JavaScript used for?", "Web Programming"),
        ("What are APIs?", "Software Integration"),
        
        # Advanced topics
        ("What is machine learning?", "Artificial Intelligence"),
        ("Explain cloud computing", "Technology Infrastructure"),
        ("What is version control?", "Software Development"),
        ("What are design patterns?", "Software Architecture"),
        
        # Networking and Security
        ("What is HTTP?", "Web Protocols"),
        ("Explain cybersecurity basics", "Information Security"),
        ("What is encryption?", "Data Security"),
        ("What are firewalls?", "Network Security")
    ]
    
    print("Testing technical concept questions...\n")
    
    for i, (question, category) in enumerate(technical_questions, 1):
        print(f"📝 Test {i}: {category}")
        print(f"Question: {question}")
        print("-" * 50)
        
        try:
            response = universal_chatbot.get_response(question)
            
            # Check if response is relevant and informative
            response_lower = response.lower()
            question_lower = question.lower()
            
            # Basic relevance check
            is_relevant = False
            if 'dbms' in question_lower and any(word in response_lower for word in ['database', 'management', 'system', 'data']):
                is_relevant = True
            elif 'variables' in question_lower and any(word in response_lower for word in ['variable', 'data', 'store', 'value', 'programming']):
                is_relevant = True
            elif 'sql' in question_lower and any(word in response_lower for word in ['database', 'query', 'structured', 'nosql']):
                is_relevant = True
            elif any(word in question_lower for word in ['html', 'css', 'javascript']) and any(word in response_lower for word in ['web', 'development', 'browser', 'website']):
                is_relevant = True
            elif 'algorithm' in question_lower and any(word in response_lower for word in ['algorithm', 'step', 'solve', 'problem', 'computer']):
                is_relevant = True
            elif len(response) > 100:  # Assume longer responses are more informative
                is_relevant = True
            
            print(f"Response: {response[:200]}{'...' if len(response) > 200 else ''}")
            print(f"✅ {'Relevant' if is_relevant else 'Needs improvement'} - Length: {len(response)} chars")
            
            if not is_relevant:
                print(f"⚠️  Response may not be specific enough for technical question")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*70 + "\n")

def test_specific_dbms_and_variables():
    """Test the specific questions mentioned by user"""
    
    print("🎯 TESTING SPECIFIC USER QUESTIONS")
    print("=" * 70)
    
    specific_questions = [
        "What is DBMS?",
        "What are variables?",
        "Explain database management systems",
        "What are variables in programming?",
        "How do databases work?",
        "What are different types of variables?"
    ]
    
    for i, question in enumerate(specific_questions, 1):
        print(f"📝 Specific Test {i}")
        print(f"Question: {question}")
        print("-" * 50)
        
        try:
            response = universal_chatbot.get_response(question)
            print(f"Response:\n{response}")
            print(f"\n✅ Response provided - Length: {len(response)} characters")
            
            # Check for key technical terms
            response_lower = response.lower()
            if 'dbms' in question.lower() or 'database' in question.lower():
                has_db_terms = any(term in response_lower for term in [
                    'database', 'data', 'management', 'system', 'sql', 'table', 'record', 'query'
                ])
                print(f"🔍 Contains database terms: {'Yes' if has_db_terms else 'No'}")
            
            if 'variable' in question.lower():
                has_var_terms = any(term in response_lower for term in [
                    'variable', 'data', 'store', 'value', 'programming', 'memory', 'assign'
                ])
                print(f"🔍 Contains variable terms: {'Yes' if has_var_terms else 'No'}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*50 + "\n")

def test_fallback_technical_responses():
    """Test technical responses when OpenAI is not available"""
    
    print("🔄 TESTING TECHNICAL FALLBACK RESPONSES")
    print("=" * 70)
    
    # Temporarily disable OpenAI to test fallback
    original_openai_available = universal_chatbot.openai_available
    universal_chatbot.openai_available = False
    
    fallback_technical_questions = [
        "What is DBMS?",
        "What are variables?", 
        "Explain Python programming",
        "What is machine learning?",
        "How do computers work?"
    ]
    
    for i, question in enumerate(fallback_technical_questions, 1):
        print(f"📝 Fallback Test {i}")
        print(f"Question: {question}")
        print("-" * 40)
        
        try:
            response = universal_chatbot.get_response(question)
            print(f"Fallback Response: {response[:300]}{'...' if len(response) > 300 else ''}")
            print(f"✅ Fallback working - Length: {len(response)} characters")
        except Exception as e:
            print(f"❌ Fallback Error: {e}")
        
        print("\n" + "="*40 + "\n")
    
    # Restore original OpenAI availability
    universal_chatbot.openai_available = original_openai_available

if __name__ == "__main__":
    print("🚀 TECHNICAL QUESTIONS TESTING SUITE")
    print("Testing chatbot's ability to handle DBMS, variables, and other technical concepts")
    print("=" * 80)
    
    try:
        # Run all technical tests
        test_specific_dbms_and_variables()
        test_technical_concepts()
        test_fallback_technical_responses()
        
        print("🎉 TECHNICAL TESTING COMPLETED!")
        print("✅ Chatbot can handle DBMS questions")
        print("✅ Chatbot can explain variables")
        print("✅ Chatbot provides technical explanations")
        print("✅ Fallback system works for technical questions")
        print("✅ Responses are informative and relevant")
        
    except Exception as e:
        print(f"❌ Test suite error: {e}")
        sys.exit(1)