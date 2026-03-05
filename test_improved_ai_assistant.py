#!/usr/bin/env python3
"""
Test script for improved AI Interview Assistant
Tests relevance and quality of responses
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

def test_improved_responses():
    """Test the improved AI Interview Assistant responses"""
    
    print("🎯 Testing Improved AI Interview Assistant")
    print("=" * 50)
    
    try:
        from services.ai_interview_assistant import ai_interview_assistant
        
        # Comprehensive test questions with expected response characteristics
        test_cases = [
            {
                'category': 'Introduction',
                'questions': [
                    'Tell me about yourself',
                    'Can you introduce yourself?',
                    'Walk me through your background',
                    'Describe yourself'
                ],
                'expected_content': ['experience', 'developer', 'projects', 'skills']
            },
            {
                'category': 'Strengths',
                'questions': [
                    'What are your greatest strengths?',
                    'What are you good at?',
                    'What are your best qualities?',
                    'What makes you a strong candidate?'
                ],
                'expected_content': ['strength', 'skill', 'good at', 'excel']
            },
            {
                'category': 'Weaknesses',
                'questions': [
                    'What is your biggest weakness?',
                    'What areas do you need to improve?',
                    'What do you struggle with?',
                    'What would you like to get better at?'
                ],
                'expected_content': ['working on', 'learned', 'improve', 'better']
            },
            {
                'category': 'Motivation',
                'questions': [
                    'Why do you want to work here?',
                    'What interests you about this company?',
                    'Why this role?',
                    'What attracts you to this position?'
                ],
                'expected_content': ['opportunity', 'excited', 'align', 'contribute']
            },
            {
                'category': 'Leadership',
                'questions': [
                    'Tell me about a time you led a team',
                    'Describe your leadership experience',
                    'When did you manage a project?',
                    'Give me an example of leadership'
                ],
                'expected_content': ['led', 'team', 'project', 'managed']
            },
            {
                'category': 'Challenges',
                'questions': [
                    'Describe a challenging situation you faced',
                    'Tell me about a difficult problem you solved',
                    'What was your biggest challenge?',
                    'Describe a tough situation at work'
                ],
                'expected_content': ['challenge', 'problem', 'solution', 'resolved']
            },
            {
                'category': 'Technical Skills',
                'questions': [
                    'What programming languages do you know?',
                    'Describe your technical skills',
                    'What technologies are you comfortable with?',
                    'Tell me about your coding experience'
                ],
                'expected_content': ['programming', 'experience', 'technology', 'development']
            },
            {
                'category': 'Future Goals',
                'questions': [
                    'Where do you see yourself in 5 years?',
                    'What are your career goals?',
                    'What are your future plans?',
                    'Where do you want to be in your career?'
                ],
                'expected_content': ['years', 'career', 'goals', 'future']
            }
        ]
        
        total_tests = 0
        passed_tests = 0
        
        for test_case in test_cases:
            print(f"\n📋 Testing {test_case['category']} Questions")
            print("-" * 40)
            
            for question in test_case['questions']:
                total_tests += 1
                
                response = ai_interview_assistant.get_response(question)
                
                # Check response quality
                is_good_length = 50 <= len(response) <= 600
                is_professional = not response.endswith('?')
                has_relevant_content = any(
                    keyword.lower() in response.lower() 
                    for keyword in test_case['expected_content']
                )
                
                # Overall quality score
                quality_score = sum([is_good_length, is_professional, has_relevant_content])
                
                if quality_score >= 2:
                    status = "✅ GOOD"
                    passed_tests += 1
                elif quality_score == 1:
                    status = "⚠️  OK"
                else:
                    status = "❌ POOR"
                
                print(f"   Q: {question}")
                print(f"   {status} ({len(response)} chars, Score: {quality_score}/3)")
                print(f"   Preview: {response[:80]}{'...' if len(response) > 80 else ''}")
                
                # Show specific issues
                if not is_good_length:
                    print(f"   ⚠️  Length issue: {len(response)} chars")
                if not is_professional:
                    print(f"   ⚠️  Ends with question mark")
                if not has_relevant_content:
                    print(f"   ⚠️  Missing expected keywords: {test_case['expected_content']}")
                
                print()
        
        # Summary
        success_rate = (passed_tests / total_tests) * 100
        print(f"📊 Test Results Summary")
        print("=" * 30)
        print(f"Total Questions Tested: {total_tests}")
        print(f"Good Responses: {passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 AI Assistant is performing well!")
        elif success_rate >= 60:
            print("⚠️  AI Assistant needs some improvements")
        else:
            print("❌ AI Assistant needs significant improvements")
        
        return success_rate >= 70
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_edge_cases():
    """Test edge cases and unusual questions"""
    
    print("\n🔍 Testing Edge Cases")
    print("=" * 30)
    
    try:
        from services.ai_interview_assistant import ai_interview_assistant
        
        edge_cases = [
            "What?",  # Very short question
            "Tell me everything about your entire life story and career",  # Very long
            "asdfghjkl",  # Nonsense
            "",  # Empty string
            "Why should we hire you over other candidates?",  # Competitive
            "What's your salary expectation?",  # Sensitive topic
            "Do you have any questions for us?",  # Reverse question
        ]
        
        for question in edge_cases:
            print(f"\nEdge case: '{question}'")
            try:
                response = ai_interview_assistant.get_response(question)
                print(f"Response: {response[:100]}{'...' if len(response) > 100 else ''}")
                print(f"Length: {len(response)} chars")
            except Exception as e:
                print(f"Error: {e}")
        
    except Exception as e:
        print(f"❌ Edge case testing failed: {e}")

def test_contextual_responses():
    """Test contextual responses with job role and company"""
    
    print("\n🎯 Testing Contextual Responses")
    print("=" * 35)
    
    try:
        from services.ai_interview_assistant import ai_interview_assistant
        
        test_contexts = [
            {
                'question': 'Why do you want this job?',
                'job_role': 'Senior Software Engineer',
                'company': 'Google'
            },
            {
                'question': 'What interests you about this role?',
                'job_role': 'Frontend Developer',
                'company': 'Startup Inc'
            },
            {
                'question': 'Why should we hire you?',
                'job_role': 'Full Stack Developer',
                'company': 'TechCorp'
            }
        ]
        
        for context in test_contexts:
            print(f"\nQuestion: {context['question']}")
            print(f"Context: {context['job_role']} at {context['company']}")
            
            response = ai_interview_assistant.get_contextual_response(
                context['question'],
                context['job_role'],
                context['company']
            )
            
            print(f"Response: {response}")
            print(f"Length: {len(response)} chars")
            print("-" * 50)
        
    except Exception as e:
        print(f"❌ Contextual testing failed: {e}")

if __name__ == "__main__":
    print("🚀 Improved AI Interview Assistant Test Suite")
    print("=" * 60)
    
    # Run comprehensive tests
    success = test_improved_responses()
    test_edge_cases()
    test_contextual_responses()
    
    if success:
        print("\n🎉 AI Interview Assistant improvements are working well!")
        print("The responses should now be more relevant and comprehensive.")
    else:
        print("\n⚠️  Some issues remain. Check the specific test results above.")