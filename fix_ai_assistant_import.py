#!/usr/bin/env python3
"""
Fix script to ensure AI Assistant is properly integrated
"""

import os
import sys

def check_files():
    """Check that all required files exist"""
    
    print("🔍 Checking AI Assistant Files")
    print("=" * 40)
    
    required_files = [
        'backend/services/ai_interview_assistant.py',
        'backend/routes/ai_assistant.py',
        'speech-analyzer-frontend/src/components/AIInterviewAssistant.jsx'
    ]
    
    all_exist = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test that imports work correctly"""
    
    print("\n🧪 Testing Imports")
    print("=" * 25)
    
    try:
        # Add backend to path
        backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
        sys.path.insert(0, backend_dir)
        
        # Test AI service import
        from services.ai_interview_assistant import ai_interview_assistant
        print("✅ AI Interview Assistant service import")
        
        # Test a quick response
        response = ai_interview_assistant.get_response("Test question")
        print(f"✅ AI service working - response length: {len(response)} chars")
        
        # Test auth middleware import
        from middleware.auth_middleware import login_required
        print("✅ Auth middleware import")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

def check_app_integration():
    """Check that the AI assistant is properly integrated in app.py"""
    
    print("\n🔗 Checking App Integration")
    print("=" * 30)
    
    try:
        with open('backend/app.py', 'r') as f:
            app_content = f.read()
        
        if 'from routes.ai_assistant import ai_assistant_bp' in app_content:
            print("✅ AI assistant import in app.py")
        else:
            print("❌ Missing AI assistant import in app.py")
            return False
        
        if 'app.register_blueprint(ai_assistant_bp)' in app_content:
            print("✅ AI assistant blueprint registered")
        else:
            print("❌ AI assistant blueprint not registered")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking app.py: {e}")
        return False

def check_frontend_integration():
    """Check that the AI assistant is integrated in the frontend"""
    
    print("\n🎨 Checking Frontend Integration")
    print("=" * 35)
    
    try:
        with open('speech-analyzer-frontend/src/components/InterviewMode.jsx', 'r') as f:
            interview_content = f.read()
        
        if 'import AIInterviewAssistant from' in interview_content:
            print("✅ AI assistant import in InterviewMode")
        else:
            print("❌ Missing AI assistant import in InterviewMode")
            return False
        
        if '<AIInterviewAssistant />' in interview_content:
            print("✅ AI assistant component used in InterviewMode")
        else:
            print("❌ AI assistant component not used in InterviewMode")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking InterviewMode.jsx: {e}")
        return False

def main():
    """Main check function"""
    
    print("🚀 AI Assistant Integration Check")
    print("=" * 50)
    
    checks = [
        check_files(),
        test_imports(),
        check_app_integration(),
        check_frontend_integration()
    ]
    
    if all(checks):
        print("\n🎉 All checks passed!")
        print("\nAI Assistant is properly integrated and ready to use.")
        print("\nTo start the system:")
        print("1. Backend: python backend/app.py")
        print("2. Frontend: npm run dev (in speech-analyzer-frontend)")
        print("3. Go to Interview Mode and click the 🎯 button")
    else:
        print("\n⚠️  Some checks failed. Please review the issues above.")

if __name__ == "__main__":
    main()