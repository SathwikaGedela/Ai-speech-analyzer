#!/usr/bin/env python3
"""
Test script for AI Interview Assistant functionality
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

def test_ai_assistant_service():
    """Test the AI Interview Assistant service"""
    
    print("🎯 Testing AI Interview Assistant Service")
    print("=" * 50)
    
    try:
        from services.ai_interview_assistant import ai_interview_assistant
        
        # Test different types of questions
        test_questions = [
            {
                'question': 'Tell me about yourself',
                'expected_keywords': ['experience', 'skills', 'passionate']
            },
            {
                'question': 'What are your greatest strengths?',
                'expected_keywords': ['strengths', 'skills', 'analytical']
            },
            {
                'question': 'Tell me about a time you showed leadership',
                'expected_keywords': ['led', 'team', 'project']
            },
            {
                'question': 'What is your biggest weakness?',
                'expected_keywords': ['working on', 'improve', 'learning']
            },
            {
                'question': 'Why do you want to work here?',
                'expected_keywords': ['opportunity', 'company', 'excited']
            }
        ]
        
        print(f"Testing {len(test_questions)} different question types...")
        
        for i, test_case in enumerate(test_questions, 1):
            question = test_case['question']
            expected_keywords = test_case['expected_keywords']
            
            print(f"\n{i}. Question: {question}")
            
            try:
                response = ai_interview_assistant.get_response(question)
                
                # Check response quality
                is_good_length = 50 <= len(response) <= 500
                has_keywords = any(keyword.lower() in response.lower() for keyword in expected_keywords)
                is_professional = not response.endswith('?')  # Should not end with question
                
                status = "✅ GOOD" if (is_good_length and is_professional) else "⚠️  BASIC"
                
                print(f"   {status} Response ({len(response)} chars)")
                print(f"   Preview: {response[:100]}{'...' if len(response) > 100 else ''}")
                
                if has_keywords:
                    print(f"   ✅ Contains relevant keywords")
                else:
                    print(f"   ⚠️  Missing expected keywords: {expected_keywords}")
                
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
        
        # Test contextual responses
        print(f"\n🎯 Testing Contextual Responses...")
        
        contextual_response = ai_interview_assistant.get_contextual_response(
            "Why do you want this job?",
            job_role="Senior Software Engineer",
            company="TechCorp"
        )
        
        print(f"   Contextual response: {contextual_response[:150]}{'...' if len(contextual_response) > 150 else ''}")
        
        print("\n✅ AI Interview Assistant service test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_api_endpoints():
    """Test the API endpoints"""
    
    print("\n🌐 Testing API Endpoints")
    print("=" * 30)
    
    try:
        import requests
        import json
        
        base_url = "http://localhost:5000"
        
        # Test endpoints (these would need authentication in real scenario)
        endpoints = [
            {
                'name': 'Practice Questions',
                'url': f'{base_url}/ai-assistant/practice-questions',
                'method': 'GET'
            },
            {
                'name': 'Interview Tips',
                'url': f'{base_url}/ai-assistant/tips',
                'method': 'GET'
            },
            {
                'name': 'AI Answer',
                'url': f'{base_url}/ai-assistant/answer',
                'method': 'POST',
                'data': {
                    'question': 'Tell me about yourself',
                    'job_role': 'Software Engineer',
                    'company': 'TechCorp'
                }
            }
        ]
        
        print("Note: These tests require the backend to be running")
        print("Run 'python backend/app.py' in another terminal first")
        
        for endpoint in endpoints:
            print(f"\n📡 Testing {endpoint['name']}...")
            
            try:
                if endpoint['method'] == 'GET':
                    response = requests.get(endpoint['url'], timeout=5)
                else:
                    response = requests.post(
                        endpoint['url'], 
                        json=endpoint['data'],
                        timeout=5
                    )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        print(f"   ✅ {endpoint['name']} working")
                    else:
                        print(f"   ⚠️  {endpoint['name']} returned error: {data.get('error', 'Unknown')}")
                else:
                    print(f"   ⚠️  {endpoint['name']} returned status {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print(f"   ⚠️  {endpoint['name']} - Backend not running")
            except Exception as e:
                print(f"   ❌ {endpoint['name']} error: {e}")
        
    except ImportError:
        print("⚠️  requests library not available. Install with: pip install requests")
    except Exception as e:
        print(f"❌ API test failed: {e}")

def test_question_coverage():
    """Test coverage of different question types"""
    
    print("\n📋 Testing Question Coverage")
    print("=" * 35)
    
    try:
        from services.ai_interview_assistant import ai_interview_assistant
        
        question_types = [
            'behavioral',
            'technical', 
            'general',
            'situational',
            'personal'
        ]
        
        sample_questions = {
            'behavioral': 'Tell me about a time you faced a challenge',
            'technical': 'What programming languages do you know?',
            'general': 'What are your strengths?',
            'situational': 'How would you handle a tight deadline?',
            'personal': 'Where do you see yourself in 5 years?'
        }
        
        for q_type in question_types:
            question = sample_questions.get(q_type, f"Sample {q_type} question")
            response = ai_interview_assistant.get_response(question)
            
            # Check if response is appropriate
            is_appropriate = (
                len(response) > 30 and 
                not response.lower().startswith('i don\'t know') and
                '?' not in response[-10:]  # Shouldn't end with questions
            )
            
            status = "✅" if is_appropriate else "⚠️"
            print(f"{status} {q_type.capitalize()}: {len(response)} chars")
        
        print("\n✅ Question coverage test completed!")
        
    except Exception as e:
        print(f"❌ Coverage test failed: {e}")

if __name__ == "__main__":
    print("🚀 AI Interview Assistant Test Suite")
    print("=" * 60)
    
    # Run tests
    service_success = test_ai_assistant_service()
    test_api_endpoints()
    test_question_coverage()
    
    if service_success:
        print("\n🎉 AI Interview Assistant is ready!")
        print("\nTo use the feature:")
        print("1. Start the backend: python backend/app.py")
        print("2. Start the frontend: npm run dev (in speech-analyzer-frontend)")
        print("3. Go to Interview Mode and look for the 🎯 button on the left")
    else:
        print("\n⚠️  Some tests failed. Check the implementation.")