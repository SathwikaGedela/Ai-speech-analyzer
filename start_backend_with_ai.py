#!/usr/bin/env python3
"""
Start backend with AI Assistant feature
"""

import os
import sys
import subprocess

def start_backend():
    """Start the backend server with AI Assistant"""
    
    print("🚀 Starting Backend with AI Assistant")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('backend/app.py'):
        print("❌ Please run this script from the project root directory")
        return False
    
    # Check that AI Assistant files exist
    required_files = [
        'backend/services/ai_interview_assistant.py',
        'backend/routes/ai_assistant.py'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing required file: {file_path}")
            return False
    
    print("✅ All AI Assistant files found")
    
    # Test imports quickly
    try:
        backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
        sys.path.insert(0, backend_dir)
        
        from services.ai_interview_assistant import ai_interview_assistant
        print("✅ AI Assistant service ready")
        
        # Quick test
        response = ai_interview_assistant.get_response("Test")
        print(f"✅ AI service working (response: {len(response)} chars)")
        
    except Exception as e:
        print(f"❌ AI Assistant import error: {e}")
        return False
    
    print("\n🎯 AI Assistant Features Available:")
    print("• Professional interview answer generation")
    print("• 40+ response variations covering all question types")
    print("• Contextual responses based on job role/company")
    print("• Practice questions library")
    print("• Interview tips and guidance")
    
    print("\n🌐 Starting Flask Backend...")
    print("Backend will be available at: http://localhost:5000")
    print("AI Assistant endpoints:")
    print("• POST /ai-assistant/answer")
    print("• GET /ai-assistant/practice-questions")
    print("• GET /ai-assistant/tips")
    
    print("\n📱 Frontend Usage:")
    print("1. Start frontend: npm run dev (in speech-analyzer-frontend)")
    print("2. Sign in to the application")
    print("3. Go to Interview Mode")
    print("4. Click the 🎯 button on the left side")
    
    print("\n" + "="*50)
    print("Starting backend server...")
    print("Press Ctrl+C to stop")
    print("="*50)
    
    # Start the backend
    try:
        os.chdir('backend')
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n🛑 Backend stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting backend: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_backend()