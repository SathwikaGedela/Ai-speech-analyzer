#!/usr/bin/env python3
"""
Test the live chatbot endpoints to ensure the fix works in the actual system
"""

import requests
import json

def test_chatbot_endpoints():
    """Test both chatbot endpoints with identity questions"""
    
    base_url = "http://localhost:5000"
    
    # Test questions that were problematic
    test_questions = [
        "what is your name",
        "are you ai", 
        "what can you do",
        "what is dbms"  # Technical question to ensure it still works
    ]
    
    # Test data for requests
    test_data = {
        "message": "",
        "context": {}
    }
    
    ai_assistant_data = {
        "question": "",
        "job_role": "",
        "company": ""
    }
    
    print("=== TESTING LIVE CHATBOT ENDPOINTS ===\n")
    
    for question in test_questions:
        print(f"Testing Question: '{question}'")
        print("-" * 60)
        
        # Test Interview Chatbot endpoint
        test_data["message"] = question
        try:
            response = requests.post(f"{base_url}/interview/chatbot", 
                                   json=test_data, 
                                   timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("✅ Interview Chatbot Response:")
                    print(data['response'][:150] + "..." if len(data['response']) > 150 else data['response'])
                else:
                    print("❌ Interview Chatbot Error:", data.get('error', 'Unknown error'))
            else:
                print(f"❌ Interview Chatbot HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Interview Chatbot Connection Error: {e}")
        
        print()
        
        # Test AI Assistant endpoint
        ai_assistant_data["question"] = question
        try:
            response = requests.post(f"{base_url}/ai-assistant/answer", 
                                   json=ai_assistant_data, 
                                   timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("✅ AI Assistant Response:")
                    print(data['answer'][:150] + "..." if len(data['answer']) > 150 else data['answer'])
                else:
                    print("❌ AI Assistant Error:", data.get('error', 'Unknown error'))
            else:
                print(f"❌ AI Assistant HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"❌ AI Assistant Connection Error: {e}")
        
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    test_chatbot_endpoints()