#!/usr/bin/env python3
"""
Debug authentication system
"""

import sys
import os
sys.path.append('backend')

from backend.app import create_app
from backend.database import db
from backend.models.user import User

def test_user_creation():
    print("🔍 Testing User Model Creation")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test creating a user
            user = User(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                phone="+1234567890"
            )
            user.set_password("password123")
            
            print("✅ User object created successfully")
            print(f"   Name: {user.first_name} {user.last_name}")
            print(f"   Email: {user.email}")
            print(f"   Phone: {user.phone}")
            print(f"   Password hash: {user.password_hash[:20]}...")
            
            # Test password verification
            if user.check_password("password123"):
                print("✅ Password verification works")
            else:
                print("❌ Password verification failed")
            
            # Test database save
            db.session.add(user)
            db.session.commit()
            print("✅ User saved to database")
            
            # Test retrieval
            retrieved_user = User.query.filter_by(email="test@example.com").first()
            if retrieved_user:
                print("✅ User retrieved from database")
                print(f"   Retrieved: {retrieved_user.first_name} {retrieved_user.last_name}")
            else:
                print("❌ User not found in database")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_user_creation()