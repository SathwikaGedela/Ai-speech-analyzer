#!/usr/bin/env python3
"""
Test AI Assistant API endpoints
"""

import requests
import json
import time

def test_endpoints():
    """Test the AI Assistant API endpoints"""
    
    print("🧪 Testing AI Assistant API Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test endpoints
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
    
    print("Note: Make sure the backend is running (python backend/app.py)")
    print("Also note: These endpoints require authentication, so they may return 401")
    print()
    
    for endpoint in endpoints:
        print(f"📡 Testing {endpoint['name']}...")
        
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(endpoint['url'], timeout=5)
            else:
                response = requests.post(
                    endpoint['url'], 
                    json=endpoint['data'],
                    timeout=5
                )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✅ {endpoint['name']} working correctly")
                    if 'practice_questions' in data:
                        print(f"   📋 Found {len(data['practice_questions'])} question categories")
                    elif 'tips' in data:
                        print(f"   💡 Found {len(data['tips'])} tip categories")
                    elif 'answer' in data:
                        print(f"   🎯 Generated answer: {data['answer'][:50]}...")
                else:
                    print(f"   ⚠️  {endpoint['name']} returned error: {data.get('error', 'Unknown')}")
            elif response.status_code == 401:
                print(f"   🔒 {endpoint['name']} requires authentication (expected)")
            else:
                print(f"   ⚠️  {endpoint['name']} returned status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {endpoint['name']} - Backend not running")
        except Exception as e:
            print(f"   ❌ {endpoint['name']} error: {e}")
        
        print()

def test_service_directly():
    """Test the AI service directly without API"""
    
    print("🎯 Testing AI Service Directly")
    print("=" * 35)
    
    try:
        import sys
        import os
        
        # Add backend directory to Python path
        backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
        sys.path.insert(0, backend_dir)
        
        from services.ai_interview_assistant import ai_interview_assistant
        
        test_questions = [
            "Tell me about yourself",
            "What are your strengths?",
            "Why do you want this job?",
            "Describe a challenge you faced"
        ]
        
        for question in test_questions:
            print(f"Q: {question}")
            response = ai_interview_assistant.get_response(question)
            print(f"A: {response[:80]}...")
            print(f"   Length: {len(response)} chars")
            print()
        
        print("✅ AI Service working correctly!")
        
    except Exception as e:
        print(f"❌ AI Service error: {e}")

if __name__ == "__main__":
    print("🚀 AI Assistant Integration Test")
    print("=" * 60)
    
    # Test service directly first
    test_service_directly()
    
    # Wait a moment
    time.sleep(1)
    
    # Test API endpoints
    test_endpoints()
    
    print("🎉 Testing complete!")
    print("\nTo use the AI Assistant:")
    print("1. Start backend: python backend/app.py")
    print("2. Start frontend: npm run dev (in speech-analyzer-frontend)")
    print("3. Sign in to the application")
    print("4. Go to Interview Mode")
    print("5. Click the 🎯 button on the left side")