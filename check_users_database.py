#!/usr/bin/env python3
"""
Check Users Database - Debug password hash issue
"""

import sys
import os
sys.path.append('backend')

from flask import Flask
from flask_cors import CORS
from database import db
from models.user import User

def check_users_database():
    """Check users in database and their password hashes"""
    
    print("🔍 Checking Users Database...")
    
    # Create a minimal Flask app to test database
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backend/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-key'
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        try:
            # Check all users
            users = User.query.all()
            print(f"✅ Found {len(users)} users in database")
            
            for user in users:
                print(f"\n--- User {user.id} ---")
                print(f"Name: {user.first_name} {user.last_name}")
                print(f"Email: {user.email}")
                print(f"Phone: {user.phone}")
                print(f"Password Hash: {user.password_hash}")
                print(f"Is Active: {user.is_active}")
                print(f"Created: {user.created_at}")
                
                # Check if password hash is None
                if user.password_hash is None:
                    print("❌ PASSWORD HASH IS NULL!")
                    
                    # Try to set a password for this user
                    print("🔧 Setting a test password...")
                    user.set_password("testpass123")
                    db.session.commit()
                    print("✅ Password set successfully")
                else:
                    print("✅ Password hash exists")
                    
                    # Test password checking
                    try:
                        result = user.check_password("testpass123")
                        print(f"✅ Password check works: {result}")
                    except Exception as e:
                        print(f"❌ Password check failed: {e}")
            
            # If no users exist, create a test user
            if len(users) == 0:
                print("\n🔧 No users found. Creating test user...")
                test_user = User(
                    first_name="Test",
                    last_name="User",
                    email="test@example.com",
                    phone="1234567890"
                )
                test_user.set_password("testpass123")
                
                db.session.add(test_user)
                db.session.commit()
                print("✅ Test user created successfully")
                
                # Test the new user
                print("🧪 Testing new user authentication...")
                auth_test = User.query.filter_by(email="test@example.com").first()
                if auth_test and auth_test.check_password("testpass123"):
                    print("✅ New user authentication works!")
                else:
                    print("❌ New user authentication failed")
                    
        except Exception as e:
            print(f"❌ Database error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == "__main__":
    check_users_database()