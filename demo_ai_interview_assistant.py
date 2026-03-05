#!/usr/bin/env python3
"""
Demo script for AI Interview Assistant
Shows the feature in action with sample questions
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

def demo_ai_interview_assistant():
    """Demonstrate the AI Interview Assistant with sample questions"""
    
    print("🎯 AI Interview Assistant Demo")
    print("=" * 50)
    print("This feature provides professional interview answers to help users practice.")
    print("It acts as a virtual interview candidate, giving direct, confident responses.\n")
    
    try:
        from services.ai_interview_assistant import ai_interview_assistant
        
        # Demo questions with different types
        demo_questions = [
            {
                'type': 'General',
                'question': 'Tell me about yourself',
                'context': 'This is the most common opening question'
            },
            {
                'type': 'Behavioral', 
                'question': 'Tell me about a time you faced a challenge',
                'context': 'Uses STAR method for structured response'
            },
            {
                'type': 'Weakness',
                'question': 'What is your biggest weakness?',
                'context': 'Shows growth mindset and self-awareness'
            },
            {
                'type': 'Technical',
                'question': 'What programming languages are you comfortable with?',
                'context': 'Demonstrates technical expertise'
            },
            {
                'type': 'Motivation',
                'question': 'Why do you want to work here?',
                'context': 'Shows genuine interest and research'
            }
        ]
        
        for i, demo in enumerate(demo_questions, 1):
            print(f"{i}. {demo['type']} Question")
            print(f"   Question: \"{demo['question']}\"")
            print(f"   Context: {demo['context']}")
            print()
            
            # Generate AI response
            response = ai_interview_assistant.get_response(demo['question'])
            
            print("   AI Answer:")
            print(f"   \"{response}\"")
            print()
            print("   " + "─" * 60)
            print()
        
        # Demo contextual response
        print("🎯 Contextual Response Demo")
        print("=" * 30)
        print("The AI can tailor responses based on job role and company:")
        print()
        
        contextual_response = ai_interview_assistant.get_contextual_response(
            "Why are you interested in this position?",
            job_role="Senior Software Engineer", 
            company="TechCorp"
        )
        
        print("Question: \"Why are you interested in this position?\"")
        print("Context: Senior Software Engineer at TechCorp")
        print()
        print("AI Answer:")
        print(f"\"{contextual_response}\"")
        print()
        
        # Usage instructions
        print("🚀 How to Use in the Application")
        print("=" * 40)
        print("1. Start the system: python start_system.py")
        print("2. Go to Interview Mode")
        print("3. Look for the 🎯 button on the left side")
        print("4. Click to open the AI Interview Assistant")
        print("5. Choose from three tabs:")
        print("   • Practice: Enter questions and get AI answers")
        print("   • Questions: Browse common interview questions")
        print("   • Tips: View interview preparation guidance")
        print()
        
        print("✨ Key Features:")
        print("• Professional, interview-ready responses")
        print("• Covers all major question types")
        print("• Optional context (job role, company)")
        print("• Comprehensive question library")
        print("• Interview tips and best practices")
        print("• No setup required - works immediately")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root directory")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    demo_ai_interview_assistant()