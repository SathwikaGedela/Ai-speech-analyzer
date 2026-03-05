#!/usr/bin/env python3
"""
Test script for Interview Chatbot functionality
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

from services.interview_chatbot import interview_chatbot

def test_chatbot_responses():
    """Test various chatbot responses"""
    
    print("🤖 Testing Interview Chatbot")
    print("=" * 50)
    
    # Test cases
    test_messages = [
        "I'm feeling nervous about my interview",
        "Can you explain the STAR method?",
        "How do I build confidence?",
        "What should I say about my weaknesses?",
        "How do I discuss salary?",
        "What questions should I ask the interviewer?",
        "Tell me about yourself tips",
        "Help me prepare",
        "Thank you for your help"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. User: {message}")
        response = interview_chatbot.get_response(message)
        print(f"   Bot: {response[:100]}{'...' if len(response) > 100 else ''}")
    
    print("\n" + "=" * 50)
    print("✅ Chatbot response test completed!")

def test_contextual_responses():
    """Test contextual responses based on interview stage"""
    
    print("\n🎯 Testing Contextual Responses")
    print("=" * 50)
    
    # Test stage responses
    stages = [
        ('question_selected', {'category': 'behavioral'}),
        ('recording_started', {}),
        ('recording_long', {}),
        ('analysis_complete', {'relevance_score': 85}),
        ('analysis_complete', {'relevance_score': 45})
    ]
    
    for stage, context in stages:
        print(f"\nStage: {stage} (context: {context})")
        response = interview_chatbot.get_stage_response(stage, **context)
        print(f"Response: {response}")
    
    print("\n" + "=" * 50)
    print("✅ Contextual response test completed!")

def test_context_updates():
    """Test context awareness"""
    
    print("\n📝 Testing Context Updates")
    print("=" * 50)
    
    # Update context
    interview_chatbot.update_context(
        selected_category='technical',
        selected_question='Walk me through your problem-solving process.',
        session_stage='practicing'
    )
    
    print("Context updated with technical question")
    
    # Test contextual help
    response = interview_chatbot._get_contextual_help()
    print(f"Contextual help: {response}")
    
    print("\n✅ Context update test completed!")

if __name__ == "__main__":
    try:
        test_chatbot_responses()
        test_contextual_responses()
        test_context_updates()
        
        print("\n🎉 All chatbot tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)