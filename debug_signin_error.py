#!/usr/bin/env python3
"""
Debug Signin Error - Check Database and User Model
"""

import sys
import os
sys.path.append('backend')

from flask import Flask
from flask_cors import CORS
from database import db
from models.user import User

def debug_signin_issue():
    """Debug the signin 500 error"""
    
    print("🔍 Debugging Signin 500 Error...")
    
    # Create a minimal Flask app to test database
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backend/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-key'
    
    # Configure CORS
    CORS(app, origins=['http://localhost:5175'], supports_credentials=True)
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        try:
            # Test 1: Check if database tables exist
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Test 2: Check if User model works
            user_count = User.query.count()
            print(f"✅ User table accessible, {user_count} users found")
            
            # Test 3: Test creating a test user
            test_email = "debug@test.com"
            existing_user = User.query.filter_by(email=test_email).first()
            
            if existing_user:
                print(f"✅ Test user already exists: {existing_user.email}")
            else:
                # Create test user
                test_user = User(
                    first_name="Debug",
                    last_name="User", 
                    email=test_email,
                    phone="1234567890"
                )
                test_user.set_password("testpass123")
                
                db.session.add(test_user)
                db.session.commit()
                print(f"✅ Test user created: {test_user.email}")
            
            # Test 4: Test authentication
            auth_user = User.query.filter_by(email=test_email).first()
            if auth_user and auth_user.check_password("testpass123"):
                print("✅ Password authentication working")
            else:
                print("❌ Password authentication failed")
            
            # Test 5: Test user.to_dict() method
            user_dict = auth_user.to_dict()
            print(f"✅ User serialization working: {user_dict}")
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n🔧 Potential Issues to Check:")
    print("1. Database file permissions")
    print("2. Missing database migrations")
    print("3. User model method errors")
    print("4. Session configuration")
    print("5. Import path issues")
    
    return True

if __name__ == "__main__":
    debug_signin_issue()