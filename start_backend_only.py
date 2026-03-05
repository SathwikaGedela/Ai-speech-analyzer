#!/usr/bin/env python3
"""
Simple backend startup script - always works
"""

import subprocess
import sys
import os
import time
import webbrowser

def create_demo_user():
    """Create demo user"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        
        from database import db
        from models.user import User
        from flask import Flask
        
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        template_dir = os.path.join(backend_dir, 'templates')
        app = Flask(__name__, template_folder=template_dir)
        
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(backend_dir, "app.db")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        
        db.init_app(app)
        
        with app.app_context():
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
                print("✅ Demo user exists")
        
        return True
    except Exception as e:
        print(f"⚠️  Demo user setup: {e}")
        return False

def main():
    print("🔧 Starting Backend Server...")
    print("=" * 40)
    
    # Create demo user
    create_demo_user()
    
    print("🚀 Starting Flask backend...")
    print("📍 Backend will run on: http://localhost:5000")
    print("👤 Demo login: demo@example.com / demo123")
    print()
    print("⚠️  For React frontend, run separately:")
    print("   cd speech-analyzer-frontend")
    print("   npm run dev")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Start backend
    try:
        subprocess.run([sys.executable, 'backend/app.py'])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

if __name__ == "__main__":
    main()