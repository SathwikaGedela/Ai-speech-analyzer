#!/usr/bin/env python3
"""
Cross-platform system startup script for Speech Analyzer
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file"""
    env_file = '.env'
    if os.path.exists(env_file):
        print("📝 Loading environment variables from .env file...")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ Environment variables loaded")
    else:
        print("⚠️  No .env file found. OpenAI features may not work.")

# Load environment variables first
load_env_file()

def check_command(command):
    """Check if a command is available"""
    try:
        subprocess.run([command, '--version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_python_deps():
    """Install Python dependencies"""
    try:
        print("📦 Installing Python dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not install Python dependencies: {e}")
        return False

def install_node_deps():
    """Install Node.js dependencies"""
    frontend_dir = Path('speech-analyzer-frontend')
    node_modules = frontend_dir / 'node_modules'
    
    if not node_modules.exists():
        try:
            print("📦 Installing Node.js dependencies...")
            subprocess.run(['npm', 'install'], 
                          cwd=frontend_dir, check=True)
            print("✅ Node.js dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Node.js dependencies: {e}")
            return False
    else:
        print("✅ Node.js dependencies already installed")
        return True

def start_backend():
    """Start the Flask backend"""
    try:
        print("🔧 Starting Backend (Flask API)...")
        if os.name == 'nt':  # Windows
            subprocess.Popen(['python', 'backend/app.py'], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Unix-like
            subprocess.Popen(['python3', 'backend/app.py'])
        return True
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the React frontend"""
    try:
        print("🎨 Starting Frontend (React)...")
        frontend_dir = Path('speech-analyzer-frontend')
        if os.name == 'nt':  # Windows
            subprocess.Popen(['npm', 'run', 'dev'], 
                           cwd=frontend_dir,
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Unix-like
            subprocess.Popen(['npm', 'run', 'dev'], cwd=frontend_dir)
        return True
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return False

def create_demo_user():
    """Create demo user if it doesn't exist"""
    try:
        # Import after ensuring backend path is available
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        
        from database import db
        from models.user import User
        from flask import Flask
        
        # Create Flask app
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        template_dir = os.path.join(backend_dir, 'templates')
        app = Flask(__name__, template_folder=template_dir)
        
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(backend_dir, "app.db")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        
        db.init_app(app)
        
        with app.app_context():
            # Check if demo user exists
            existing_user = User.query.filter_by(email='demo@example.com').first()
            if not existing_user:
                user = User(
                    first_name='Demo',
                    last_name='User',
                    email='demo@example.com',
                    phone='1234567890'
                )
                user.set_password('demo123')
                
                db.session.add(user)
                db.session.commit()
                print("✅ Created demo user")
            else:
                print("✅ Demo user already exists")
        
        return True
    except Exception as e:
        print(f"⚠️  Could not create demo user: {e}")
        return False

def main():
    print("=" * 50)
    print("   🎤 Speech Analyzer System Startup")
    print("=" * 50)
    print()
    
    # Check prerequisites
    if not check_command('python'):
        print("❌ Python is not installed or not in PATH")
        print("Please install Python and try again")
        return False
    
    if not check_command('node'):
        print("❌ Node.js is not installed or not in PATH")
        print("Please install Node.js and try again")
        return False
    
    if not check_command('npm'):
        print("❌ npm is not available")
        print("Please install Node.js with npm and try again")
        return False
    
    print("✅ Python and Node.js are available")
    print()
    
    # Install dependencies
    install_python_deps()
    if not install_node_deps():
        return False
    
    print()
    print("🚀 Starting services...")
    print()
    
    # Create demo user
    create_demo_user()
    
    # Start services
    if not start_backend():
        return False
    
    time.sleep(3)  # Wait for backend to start
    
    if not start_frontend():
        return False
    
    time.sleep(5)  # Wait for frontend to start
    
    print()
    print("=" * 50)
    print("   🎉 System Started Successfully!")
    print("=" * 50)
    print()
    print("🔗 Backend API: http://localhost:5000")
    print("🌐 Frontend:    http://localhost:5173")
    print()
    print("👤 Demo Login Credentials:")
    print("   Email:    demo@example.com")
    print("   Password: demo123")
    print()
    print("🌐 Opening browser...")
    
    # Open browser
    try:
        webbrowser.open('http://localhost:5173')
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("Please open http://localhost:5173 manually")
    
    print()
    print("✅ System is running!")
    print("   Keep this window open or press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        return True

if __name__ == "__main__":
    success = main()
    if not success:
        input("\nPress Enter to exit...")
        sys.exit(1)