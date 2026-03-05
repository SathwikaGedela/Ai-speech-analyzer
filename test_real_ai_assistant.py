#!/usr/bin/env python3
"""
Test script for Real AI Interview Assistant
"""

import sys
import os
import time

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

def test_ai_model_loading():
    """Test AI model loading and initialization"""
    
    print("🤖 Testing Real AI Model Loading")
    print("=" * 50)
    
    try:
        from services.real_ai_assistant import real_ai_assistant
        
        # Get model info
        model_info = real_ai_assistant.get_model_info()
        
        print("Model Information:")
        print(f"• Model Loaded: {model_info['model_loaded']}")
        print(f"• Model Name: {model_info['model_name']}")
        print(f"• Device: {model_info['device']}")
        print(f"• AI Powered: {model_info['ai_powered']}")
        
        if 'parameters' in model_info:
            print(f"• Parameters: {model_info['parameters']}")
        
        return model_info['model_loaded']
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: python install_ai_dependencies.py")
        return False
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False

def test_ai_responses():
    """Test AI response generation"""
    
    print("\n🧪 Testing AI Response Generation")
    print("=" * 45)
    
    try:
        from services.real_ai_assistant import real_ai_assistant
        
        test_questions = [
            {
                'question': 'Tell me about yourself',
                'expected_topics': ['experience', 'skills', 'developer']
            },
            {
                'question': 'What are your greatest strengths?',
                'expected_topics': ['strength', 'skill', 'good']
            },
            {
                'question': 'Why do you want this job?',
                'expected_topics': ['opportunity', 'company', 'role']
            },
            {
                'question': 'Describe a challenging project you worked on',
                'expected_topics': ['project', 'challenge', 'solution']
            }
        ]
        
        ai_responses = 0
        total_questions = len(test_questions)
        
        for i, test_case in enumerate(test_questions, 1):
            question = test_case['question']
            
            print(f"\n{i}. Question: {question}")
            
            start_time = time.time()
            response = real_ai_assistant.get_response(question)
            generation_time = time.time() - start_time
            
            print(f"   Response ({generation_time:.2f}s): {response[:100]}{'...' if len(response) > 100 else ''}")
            print(f"   Length: {len(response)} characters")
            
            # Check if response seems AI-generated (not just fallback)
            model_info = real_ai_assistant.get_model_info()
            if model_info['ai_powered'] and len(response) > 50 and not response.startswith("I believe my combination"):
                ai_responses += 1
                print("   ✅ AI-generated response")
            else:
                print("   📝 Fallback response")
        
        print(f"\n📊 Results: {ai_responses}/{total_questions} AI-generated responses")
        
        if ai_responses > 0:
            print("🎉 Real AI is working!")
        else:
            print("⚠️  Using fallback responses (AI model may not be loaded)")
        
        return ai_responses > 0
        
    except Exception as e:
        print(f"❌ Response generation error: {e}")
        return False

def test_contextual_responses():
    """Test contextual AI responses"""
    
    print("\n🎯 Testing Contextual Responses")
    print("=" * 40)
    
    try:
        from services.real_ai_assistant import real_ai_assistant
        
        test_contexts = [
            {
                'question': 'Why are you interested in this position?',
                'job_role': 'Senior Software Engineer',
                'company': 'Google'
            },
            {
                'question': 'What makes you a good fit for this role?',
                'job_role': 'Frontend Developer',
                'company': 'Startup Inc'
            }
        ]
        
        for i, context in enumerate(test_contexts, 1):
            print(f"\n{i}. Question: {context['question']}")
            print(f"   Context: {context['job_role']} at {context['company']}")
            
            response = real_ai_assistant.get_contextual_response(
                context['question'],
                context['job_role'],
                context['company']
            )
            
            print(f"   Response: {response[:120]}{'...' if len(response) > 120 else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ Contextual response error: {e}")
        return False

def test_performance():
    """Test AI response performance"""
    
    print("\n⚡ Testing Performance")
    print("=" * 30)
    
    try:
        from services.real_ai_assistant import real_ai_assistant
        
        # Test multiple responses for timing
        test_question = "What are your career goals?"
        times = []
        
        print("Generating 3 responses to measure performance...")
        
        for i in range(3):
            start_time = time.time()
            response = real_ai_assistant.get_response(test_question)
            end_time = time.time()
            
            generation_time = end_time - start_time
            times.append(generation_time)
            
            print(f"Response {i+1}: {generation_time:.2f}s ({len(response)} chars)")
        
        avg_time = sum(times) / len(times)
        print(f"\nAverage generation time: {avg_time:.2f}s")
        
        if avg_time < 5:
            print("✅ Good performance")
        elif avg_time < 15:
            print("⚠️  Moderate performance (consider GPU acceleration)")
        else:
            print("🐌 Slow performance (GPU recommended)")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 Real AI Interview Assistant Test Suite")
    print("=" * 60)
    
    # Run tests
    tests = [
        test_ai_model_loading(),
        test_ai_responses(),
        test_contextual_responses(),
        test_performance()
    ]
    
    passed_tests = sum(tests)
    total_tests = len(tests)
    
    print(f"\n📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Real AI Interview Assistant is ready!")
    elif passed_tests > 0:
        print("⚠️  Some tests passed. AI is partially working.")
    else:
        print("❌ Tests failed. Check AI dependencies.")
        print("Run: python install_ai_dependencies.py")
    
    print("\n💡 Usage Tips:")
    print("• First AI response may be slower (model loading)")
    print("• Subsequent responses are faster (model cached)")
    print("• GPU significantly improves performance")
    print("• Fallback responses work if AI fails")

if __name__ == "__main__":
    main()