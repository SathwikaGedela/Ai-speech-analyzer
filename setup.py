"""
Setup script for AI Public Speaking Feedback System
Run this script to set up the project environment
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.download('brown', quiet=True)
        print("✅ NLTK data downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = ['uploads', 'audio', 'static', 'templates']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   Created: {directory}/")
        else:
            print(f"   Exists: {directory}/")
    
    print("✅ Directories ready!")
    return True

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    required_modules = [
        'flask',
        'speech_recognition',
        'textblob',
        'pydub',
        'nltk'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("✅ All imports successful!")
        return True

def main():
    """Main setup function"""
    print("🚀 AI Public Speaking Feedback System Setup")
    print("=" * 50)
    
    steps = [
        ("Installing packages", install_requirements),
        ("Creating directories", create_directories),
        ("Downloading NLTK data", download_nltk_data),
        ("Testing imports", test_imports)
    ]
    
    all_success = True
    
    for step_name, step_function in steps:
        print(f"\n{step_name}...")
        if not step_function():
            all_success = False
            break
    
    print("\n" + "=" * 50)
    
    if all_success:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run demo test: python demo_test.py")
        print("2. Generate test audio: python test_audio_generator.py")
        print("3. Start web app: python app.py")
        print("4. Open browser: http://127.0.0.1:5000")
    else:
        print("❌ Setup failed. Please check the errors above.")
        print("You may need to install Python packages manually:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()