#!/usr/bin/env python3
"""
Test the chatbot endpoints directly without authentication for debugging
"""

import sys
import os
sys.path.append('backend')

# Import the Flask app and test client
from backend.app import app

def test_chatbot_responses():
    """Test chatbot responses using Flask test client"""
    
    with app.test_client() as client:
        # Mock authentication by setting session
        with client.session_transaction() as sess:
            sess['user_id'] = 1  # Mock user ID
            sess['logged_in'] = True
        
        test_questions = [
            "what is your name",
            "are you ai", 
            "what can you do",
            "what is dbms"
        ]
        
        print("=== TESTING CHATBOT ENDPOINTS ===\n")
        
        for question in test_questions:
            print(f"Testing: '{question}'")
            print("-" * 50)
            
            # Test Interview Chatbot
            response = client.post('/interview/chatbot', 
                                 json={'message': question, 'context': {}})
            
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    print("✅ Interview Chatbot:")
                    print(data['response'][:200] + "..." if len(data['response']) > 200 else data['response'])
                else:
                    print("❌ Interview Error:", data.get('error'))
            else:
                print(f"❌ Interview HTTP Error: {response.status_code}")
            
            print()
            
            # Test AI Assistant
            response = client.post('/ai-assistant/answer', 
                                 json={'question': question})
            
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success'):
                    print("✅ AI Assistant:")
                    print(data['answer'][:200] + "..." if len(data['answer']) > 200 else data['answer'])
                else:
                    print("❌ AI Assistant Error:", data.get('error'))
            else:
                print(f"❌ AI Assistant HTTP Error: {response.status_code}")
            
            print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_chatbot_responses()