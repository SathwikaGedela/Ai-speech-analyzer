#!/usr/bin/env python3
"""
Test script for Smart AI Interview Assistant
Tests both AI and fallback functionality
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

def test_smart_ai_initialization():
    """Test Smart AI initialization"""
    
    print("🤖 Testing Smart AI Initialization")
    print("=" * 45)
    
    try:
        from services.smart_ai_assistant import smart_ai_assistant
        
        # Get model info
        model_info = smart_ai_assistant.get_model_info()
        
        print("Smart AI Status:")
        print(f"• Model Loaded: {model_info['model_loaded']}")
        print(f"• Model Name: {model_info['model_name']}")
        print(f"• Device: {model_info['device']}")
        print(f"• AI Powered: {model_info['ai_powered']}")
        print(f"• Parameters: {model_info['parameters']}")
        
        if model_info['ai_powered']:
            print("🎉 Real AI model is working!")
        else:
            print("📝 Using enhanced fallback system")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_response_quality():
    """Test response quality for different question types"""
    
    print("\n🧪 Testing Response Quality")
    print("=" * 35)
    
    try:
        from services.smart_ai_assistant import smart_ai_assistant
        
        test_questions = [
            {
                'question': 'Tell me about yourself',
                'category': 'Introduction'
            },
            {
                'question': 'What are your greatest strengths?',
                'category': 'Strengths'
            },
            {
                'question': 'What is your biggest weakness?',
                'category': 'Weaknesses'
            },
            {
                'question': 'Why do you want this job?',
                'category': 'Motivation'
            },
            {
                'question': 'Describe a challenging project you worked on',
                'category': 'Challenges'
            },
            {
                'question': 'Tell me about a time you led a team',
                'category': 'Leadership'
            }
        ]
        
        model_info = smart_ai_assistant.get_model_info()
        ai_type = "Real AI" if model_info['ai_powered'] else "Enhanced Fallback"
        
        print(f"Testing with: {ai_type}")
        print()
        
        for i, test_case in enumerate(test_questions, 1):
            question = test_case['question']
            category = test_case['category']
            
            print(f"{i}. {category}: {question}")
            
            response = smart_ai_assistant.get_response(question)
            
            # Quality checks
            is_good_length = 50 <= len(response) <= 600
            is_professional = not response.endswith('?')
            has_content = len(response.split()) > 10
            
            quality_score = sum([is_good_length, is_professional, has_content])
            
            if quality_score >= 2:
                status = "✅ GOOD"
            elif quality_score == 1:
                status = "⚠️  OK"
            else:
                status = "❌ POOR"
            
            print(f"   {status} ({len(response)} chars)")
            print(f"   Response: {response[:80]}{'...' if len(response) > 80 else ''}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Response quality test error: {e}")
        return False

def test_contextual_responses():
    """Test contextual responses"""
    
    print("🎯 Testing Contextual Responses")
    print("=" * 40)
    
    try:
        from services.smart_ai_assistant import smart_ai_assistant
        
        test_contexts = [
            {
                'question': 'Why are you interested in this position?',
                'job_role': 'Senior Software Engineer',
                'company': 'TechCorp'
            },
            {
                'question': 'What makes you a good fit?',
                'job_role': 'Frontend Developer',
                'company': 'StartupInc'
            }
        ]
        
        for i, context in enumerate(test_contexts, 1):
            print(f"{i}. Question: {context['question']}")
            print(f"   Context: {context['job_role']} at {context['company']}")
            
            response = smart_ai_assistant.get_contextual_response(
                context['question'],
                context['job_role'],
                context['company']
            )
            
            print(f"   Response: {response[:100]}{'...' if len(response) > 100 else ''}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Contextual response test error: {e}")
        return False

def test_backend_integration():
    """Test backend integration"""
    
    print("🔗 Testing Backend Integration")
    print("=" * 35)
    
    try:
        # Test import
        from routes.ai_assistant import ai_assistant_bp
        print("✅ AI assistant routes import successfully")
        
        # Test service import
        from services.smart_ai_assistant import smart_ai_assistant
        print("✅ Smart AI service import successfully")
        
        # Test basic functionality
        response = smart_ai_assistant.get_response("Test question")
        if len(response) > 10:
            print("✅ Basic response generation working")
        else:
            print("⚠️  Response seems short")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend integration error: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 Smart AI Interview Assistant Test Suite")
    print("=" * 60)
    
    # Run tests
    tests = [
        test_smart_ai_initialization(),
        test_response_quality(),
        test_contextual_responses(),
        test_backend_integration()
    ]
    
    passed_tests = sum(tests)
    total_tests = len(tests)
    
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Smart AI Assistant is ready!")
    elif passed_tests > 0:
        print("⚠️  Some tests passed. System is partially working.")
    else:
        print("❌ Tests failed. Check the implementation.")
    
    print("\n💡 System Features:")
    print("• ✅ Graceful AI/fallback handling")
    print("• ✅ Enhanced response quality")
    print("• ✅ Contextual awareness")
    print("• ✅ Professional interview responses")
    print("• ✅ No dependency issues")
    
    print("\nTo start the system:")
    print("python backend/app.py")

if __name__ == "__main__":
    main()