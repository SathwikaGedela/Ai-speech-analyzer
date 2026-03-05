#!/usr/bin/env python3
"""
Fix signin issue by resetting test user and verifying database
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

def reset_test_user():
    """Reset test user with proper password"""
    app = create_app()
    
    with app.app_context():
        # Delete existing test user
        existing_user = User.query.filter_by(email='test@example.com').first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()
            print("🗑️ Deleted existing test user")
        
        # Create new test user
        user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone='1234567890'
        )
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        print("✅ Created new test user")
        print(f"   Email: {user.email}")
        print(f"   Password: password123")
        print(f"   ID: {user.id}")
        
        # Verify password works
        if user.check_password('password123'):
            print("✅ Password verification successful")
        else:
            print("❌ Password verification failed")
        
        return user

def test_database_connection():
    """Test database connection and user operations"""
    app = create_app()
    
    with app.app_context():
        try:
            # Test database connection
            users = User.query.all()
            print(f"📊 Database connection successful. Found {len(users)} users.")
            
            # List all users
            for user in users:
                print(f"   - {user.email} (ID: {user.id})")
            
            return True
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False

def main():
    print("🔧 Fixing signin issue...")
    print("=" * 50)
    
    if test_database_connection():
        reset_test_user()
        print("\n✅ Test user reset complete. Try signing in again.")
    else:
        print("❌ Database connection failed")

if __name__ == "__main__":
    main()