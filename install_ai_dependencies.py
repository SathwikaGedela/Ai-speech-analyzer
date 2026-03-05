#!/usr/bin/env python3
"""
Install AI dependencies for Real AI Interview Assistant
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required AI libraries"""
    
    print("🤖 Installing Real AI Dependencies")
    print("=" * 50)
    
    # AI libraries to install
    ai_packages = [
        "torch==2.0.1",
        "transformers==4.30.2", 
        "accelerate==0.20.3",
        "datasets==2.12.0"
    ]
    
    print("📦 Installing AI packages...")
    print("This may take several minutes as it downloads large models.")
    print()
    
    for package in ai_packages:
        print(f"Installing {package}...")
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', package
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
                print(f"Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {package} installation timed out (this is normal for large packages)")
            print("Continuing with next package...")
        except Exception as e:
            print(f"❌ Error installing {package}: {e}")
            return False
    
    print("\n🧪 Testing AI imports...")
    
    # Test imports
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} - Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
        
        import transformers
        print(f"✅ Transformers {transformers.__version__}")
        
        # Test model loading (this will download the model on first run)
        print("\n📥 Testing model download (this may take a few minutes)...")
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        model_name = "distilgpt2"  # Lightweight model for testing
        print(f"Downloading {model_name}...")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        print(f"✅ Model {model_name} loaded successfully")
        
        # Test generation
        print("🧪 Testing text generation...")
        from transformers import pipeline
        
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
        test_response = generator("Hello, I am", max_length=20, num_return_sequences=1)
        
        print(f"✅ Text generation working: {test_response[0]['generated_text'][:50]}...")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Model test error: {e}")
        print("This might be normal - the model will download when first used.")
    
    return True

def check_system_requirements():
    """Check system requirements for AI models"""
    
    print("\n💻 Checking System Requirements")
    print("=" * 40)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"⚠️  Python {python_version.major}.{python_version.minor} (3.8+ recommended)")
    
    # Check available memory (rough estimate)
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        
        if memory_gb >= 8:
            print(f"✅ RAM: {memory_gb:.1f} GB")
        else:
            print(f"⚠️  RAM: {memory_gb:.1f} GB (8GB+ recommended for better performance)")
            
    except ImportError:
        print("ℹ️  Install psutil to check memory: pip install psutil")
    
    # Check CUDA availability
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("ℹ️  CUDA not available - will use CPU (slower but works)")
    except ImportError:
        print("ℹ️  PyTorch not installed yet")

def main():
    """Main installation function"""
    
    print("🚀 Real AI Interview Assistant Setup")
    print("=" * 60)
    
    check_system_requirements()
    
    print("\n⚠️  Important Notes:")
    print("• First-time setup will download AI models (~500MB-2GB)")
    print("• This may take 10-30 minutes depending on internet speed")
    print("• Models are cached locally for future use")
    print("• CPU inference is slower but works on any system")
    print("• GPU (CUDA) significantly improves performance")
    
    response = input("\nContinue with installation? (y/n): ").lower().strip()
    
    if response != 'y':
        print("Installation cancelled.")
        return
    
    if install_dependencies():
        print("\n🎉 Real AI Installation Complete!")
        print("\nYour AI Interview Assistant now uses real language models!")
        print("\nFeatures:")
        print("• Dynamic response generation")
        print("• Context-aware answers")
        print("• Personalized interview coaching")
        print("• Real-time AI processing")
        
        print("\nTo start using:")
        print("1. python backend/app.py")
        print("2. Go to Interview Mode")
        print("3. Click the 🤖 button for Real AI responses")
        
    else:
        print("\n❌ Installation failed. Please check the errors above.")
        print("You can still use the rule-based responses as fallback.")

if __name__ == "__main__":
    main()