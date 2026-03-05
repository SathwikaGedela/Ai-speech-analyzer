#!/usr/bin/env python3
"""
Create a demo user for testing the React frontend
"""

import sys
import os

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

from database import db
from models.user import User
from flask import Flask

def create_app():
    """Create Flask app for database operations"""
    template_dir = os.path.join(backend_dir, 'templates')
    app = Flask(__name__, template_folder=template_dir)
    
    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(backend_dir, "app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    return app

def create_demo_user():
    """Create a demo user for testing"""
    app = create_app()
    
    with app.app_context():
        # Delete existing demo user
        existing_user = User.query.filter_by(email='demo@example.com').first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            print("🗑️ Deleted existing demo user")
        
        # Create new demo user
        user = User(
            first_name='Demo',
            last_name='User',
            email='demo@example.com',
            phone='1234567890'
        )
        user.set_password('demo123')
        
        db.session.add(user)
        db.session.commit()
        
        print("✅ Created demo user for testing")
        print("=" * 40)
        print("📧 Email: demo@example.com")
        print("🔑 Password: demo123")
        print("=" * 40)
        print("You can now use these credentials to sign in!")
        
        return user

if __name__ == "__main__":
    create_demo_user()