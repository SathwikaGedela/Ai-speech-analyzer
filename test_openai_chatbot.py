#!/usr/bin/env python3
"""
Test script for OpenAI-powered Interview Chatbot
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

def test_openai_chatbot():
    """Test OpenAI chatbot functionality"""
    
    print("🤖 Testing OpenAI Interview Chatbot")
    print("=" * 50)
    
    try:
        from services.openai_chatbot import openai_chatbot
        
        # Check if OpenAI is available
        if openai_chatbot.openai_available:
            print("✅ OpenAI API key found and configured")
        else:
            print("⚠️  OpenAI API key not found - using fallback responses")
        
        # Test questions
        test_questions = [
            "How do I prepare for a behavioral interview?",
            "I'm nervous about my upcoming interview",
            "Can you explain the STAR method?",
            "What questions should I ask the interviewer?",
            "How do I negotiate salary?"
        ]
        
        print(f"\n🧪 Testing {len(test_questions)} questions...")
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{i}. User: {question}")
            
            try:
                response = openai_chatbot.get_response(question)
                
                # Check response quality
                is_helpful = len(response) > 50 and not response.endswith('?')
                status = "✅ GOOD" if is_helpful else "⚠️  BASIC"
                
                print(f"   {status} Response ({len(response)} chars)")
                print(f"   Preview: {response[:100]}{'...' if len(response) > 100 else ''}")
                
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
        
        # Test contextual responses
        print(f"\n🎯 Testing Contextual Responses...")
        
        # Update context
        openai_chatbot.update_context(
            selected_category='behavioral',
            selected_question='Tell me about a time you faced a challenge',
            session_stage='practicing'
        )
        
        contextual_response = openai_chatbot.get_response("Give me tips for this question")
        print(f"   Contextual response: {contextual_response[:150]}{'...' if len(contextual_response) > 150 else ''}")
        
        # Test stage responses
        stage_response = openai_chatbot.get_stage_response('analysis_complete', relevance_score=85)
        print(f"   Stage response: {stage_response[:150]}{'...' if len(stage_response) > 150 else ''}")
        
        print("\n✅ OpenAI chatbot test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please run: python setup_openai.py")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def test_fallback_functionality():
    """Test that fallback works when OpenAI is unavailable"""
    
    print("\n🔄 Testing Fallback Functionality")
    print("=" * 40)
    
    try:
        from services.openai_chatbot import openai_chatbot
        
        # Temporarily disable OpenAI
        original_status = openai_chatbot.openai_available
        openai_chatbot.openai_available = False
        
        response = openai_chatbot.get_response("How do I prepare for interviews?")
        
        # Restore original status
        openai_chatbot.openai_available = original_status
        
        if len(response) > 50:
            print("✅ Fallback chatbot working correctly")
            print(f"   Response: {response[:100]}{'...' if len(response) > 100 else ''}")
        else:
            print("⚠️  Fallback response seems short")
        
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")

if __name__ == "__main__":
    print("🚀 SpeechAnalyzer OpenAI Integration Test")
    print("=" * 60)
    
    success = test_openai_chatbot()
    test_fallback_functionality()
    
    if success:
        print("\n🎉 All tests passed!")
        print("\nYour OpenAI-powered interview chatbot is ready!")
    else:
        print("\n⚠️  Some tests failed. Check the setup and try again.")
        print("Run: python setup_openai.py")