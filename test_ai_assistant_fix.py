#!/usr/bin/env python3
"""
Test AI Assistant Fix - Verify it now uses universal chatbot
"""

import requests
import json

def test_ai_assistant_endpoint():
    """Test the AI assistant endpoint with various questions"""
    
    print("🔧 TESTING AI ASSISTANT ENDPOINT FIX")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    test_questions = [
        "What is DBMS?",
        "What are variables?",
        "Tell me about yourself",
        "What are your strengths?",
        "What is artificial intelligence?",
        "How do I prepare for interviews?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"📝 Test {i}")
        print(f"Question: {question}")
        print("-" * 40)
        
        try:
            response = requests.post(
                f"{base_url}/ai-assistant/answer",
                json={
                    "question": question,
                    "job_role": "Software Developer",
                    "company": "Tech Company"
                },
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    answer = data.get('answer', '')
                    
                    # Check if we got a good response (not the generic one)
                    if "technical expertise, problem-solving skills" in answer:
                        print("❌ Still getting generic response!")
                    elif len(answer) > 200 and ('**' in answer or '•' in answer):
                        print("✅ Got comprehensive response!")
                    else:
                        print("👍 Got relevant response")
                    
                    print(f"Response: {answer[:150]}...")
                    print(f"Length: {len(answer)} characters")
                else:
                    print(f"❌ API error: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Backend server not running")
            print("💡 Start with: python backend/app.py")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    test_ai_assistant_endpoint()