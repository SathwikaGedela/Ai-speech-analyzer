#!/usr/bin/env python3
"""
Setup script for OpenAI integration
"""

import os
import sys

def setup_openai():
    """Setup OpenAI API key and test connection"""
    
    print("🤖 OpenAI Integration Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = '.env'
    env_example = '.env.example'
    
    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            print("📝 Creating .env file from template...")
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ .env file created")
        else:
            print("❌ .env.example not found")
            return False
    
    # Get API key from user
    print("\n🔑 OpenAI API Key Setup")
    print("To get your API key:")
    print("1. Go to https://platform.openai.com/api-keys")
    print("2. Sign in or create an account")
    print("3. Click 'Create new secret key'")
    print("4. Copy the key (starts with 'sk-')")
    
    api_key = input("\nEnter your OpenAI API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️  Skipping OpenAI setup. Chatbot will use fallback responses.")
        return True
    
    if not api_key.startswith('sk-'):
        print("❌ Invalid API key format. Should start with 'sk-'")
        return False
    
    # Update .env file
    try:
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Update or add OPENAI_API_KEY
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('OPENAI_API_KEY='):
                lines[i] = f'OPENAI_API_KEY={api_key}\n'
                updated = True
                break
        
        if not updated:
            lines.append(f'OPENAI_API_KEY={api_key}\n')
        
        with open(env_file, 'w') as f:
            f.writelines(lines)
        
        print("✅ API key saved to .env file")
        
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        return False
    
    # Test the API key
    print("\n🧪 Testing OpenAI connection...")
    
    try:
        os.environ['OPENAI_API_KEY'] = api_key
        
        # Import and test
        import openai
        openai.api_key = api_key
        
        # Simple test call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print("✅ OpenAI connection successful!")
        print("🎉 Your chatbot is now powered by GPT!")
        
    except ImportError:
        print("⚠️  OpenAI library not installed. Run: pip install openai==0.28.1")
        return False
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        print("Please check your API key and try again.")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies"""
    
    print("\n📦 Installing Dependencies")
    print("=" * 30)
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'openai==0.28.1'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ OpenAI library installed successfully")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def main():
    """Main setup function"""
    
    print("🚀 SpeechAnalyzer OpenAI Integration Setup")
    print("=" * 60)
    
    # Install dependencies first
    if not install_dependencies():
        print("\n❌ Setup failed. Please install dependencies manually:")
        print("pip install openai==0.28.1")
        return
    
    # Setup OpenAI
    if setup_openai():
        print("\n🎉 Setup Complete!")
        print("\nYour interview chatbot is now enhanced with OpenAI GPT!")
        print("The chatbot will provide more intelligent, conversational responses.")
        print("\nTo start the system:")
        print("python start_system.py")
    else:
        print("\n⚠️  Setup completed with warnings.")
        print("The chatbot will work with fallback responses.")

if __name__ == "__main__":
    main()