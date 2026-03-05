#!/usr/bin/env python3
"""
Start system with Real AI Interview Assistant
"""

import os
import sys
import subprocess
import time

def check_ai_status():
    """Check if AI models are available"""
    
    print("🤖 Checking Real AI Status")
    print("=" * 40)
    
    try:
        # Add backend to path
        backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
        sys.path.insert(0, backend_dir)
        
        from services.real_ai_assistant import real_ai_assistant
        
        # Get model info
        model_info = real_ai_assistant.get_model_info()
        
        print(f"✅ AI Model: {model_info['model_name']}")
        print(f"✅ Device: {model_info['device']}")
        print(f"✅ AI Powered: {model_info['ai_powered']}")
        
        if model_info['ai_powered']:
            print("🎉 Real AI is ready!")
            
            # Quick test
            print("\n🧪 Testing AI response...")
            response = real_ai_assistant.get_response("What are your strengths?")
            print(f"Sample response: {response[:80]}...")
            
        return model_info['ai_powered']
        
    except ImportError as e:
        print(f"❌ AI dependencies missing: {e}")
        print("Run: python install_ai_dependencies.py")
        return False
    except Exception as e:
        print(f"⚠️  AI initialization issue: {e}")
        print("Will use fallback responses")
        return False

def start_system():
    """Start the complete system"""
    
    print("🚀 Starting Real AI Interview System")
    print("=" * 50)
    
    # Check AI status
    ai_available = check_ai_status()
    
    print(f"\n🎯 System Features:")
    if ai_available:
        print("• ✅ Real AI-powered interview responses")
        print("• ✅ Dynamic, contextual answer generation")
        print("• ✅ Personalized interview coaching")
        print("• ✅ Natural language understanding")
    else:
        print("• 📝 Rule-based interview responses (fallback)")
        print("• ⚠️  Install AI dependencies for full features")
    
    print("• ✅ Speech analysis and feedback")
    print("• ✅ Interview practice mode")
    print("• ✅ Progress tracking and history")
    print("• ✅ User authentication and profiles")
    
    print(f"\n🌐 Starting Backend Server...")
    print("Backend will be available at: http://localhost:5000")
    
    if ai_available:
        print("🤖 Real AI endpoints active:")
    else:
        print("📝 Fallback AI endpoints active:")
        
    print("• POST /ai-assistant/answer")
    print("• GET /ai-assistant/model-info")
    print("• GET /ai-assistant/practice-questions")
    print("• GET /ai-assistant/tips")
    
    print(f"\n📱 Frontend Usage:")
    print("1. Start frontend: npm run dev (in speech-analyzer-frontend)")
    print("2. Sign in to the application")
    print("3. Go to Interview Mode")
    if ai_available:
        print("4. Click the 🤖 button for Real AI responses")
    else:
        print("4. Click the 🤖 button for interview assistance")
    
    print("\n" + "="*50)
    print("Starting backend server...")
    print("Press Ctrl+C to stop")
    print("="*50)
    
    # Start the backend
    try:
        os.chdir('backend')
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n🛑 System stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting system: {e}")

if __name__ == "__main__":
    start_system()