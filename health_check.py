#!/usr/bin/env python3
"""
Health check script to verify both backend and frontend are running
"""

import requests
import time
import sys

def check_backend():
    """Check if backend is running and responsive"""
    try:
        response = requests.get('http://localhost:5000/api/user', timeout=5)
        if response.status_code in [200, 401]:  # 401 is expected when not authenticated
            print("✅ Backend is running (http://localhost:5000)")
            return True
        else:
            print(f"⚠️  Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running (http://localhost:5000)")
        return False
    except Exception as e:
        print(f"❌ Backend check failed: {e}")
        return False

def check_frontend():
    """Check if frontend is running"""
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running (http://localhost:5173)")
            return True
        else:
            print(f"⚠️  Frontend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running (http://localhost:5173)")
        return False
    except Exception as e:
        print(f"❌ Frontend check failed: {e}")
        return False

def test_signin():
    """Test signin functionality"""
    try:
        signin_data = {
            "email": "demo@example.com",
            "password": "demo123"
        }
        
        response = requests.post(
            'http://localhost:5000/api/signin',
            json=signin_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Signin functionality working")
            return True
        elif response.status_code == 401:
            print("⚠️  Demo user credentials invalid (run: python create_demo_user.py)")
            return False
        else:
            print(f"❌ Signin failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Signin test failed: {e}")
        return False

def main():
    print("🔍 Health Check - Speech Analyzer System")
    print("=" * 45)
    print()
    
    backend_ok = check_backend()
    frontend_ok = check_frontend()
    
    print()
    
    if backend_ok and frontend_ok:
        print("🎉 System Status: HEALTHY")
        print()
        print("Testing signin functionality...")
        signin_ok = test_signin()
        
        if signin_ok:
            print()
            print("✅ All systems operational!")
            print("🌐 Open: http://localhost:5173")
            print("👤 Login: demo@example.com / demo123")
        else:
            print()
            print("⚠️  System running but signin has issues")
            print("💡 Try: python create_demo_user.py")
    
    elif backend_ok and not frontend_ok:
        print("⚠️  System Status: PARTIAL")
        print("💡 Frontend not running. Start with:")
        print("   cd speech-analyzer-frontend && npm run dev")
    
    elif not backend_ok and frontend_ok:
        print("⚠️  System Status: PARTIAL") 
        print("💡 Backend not running. Start with:")
        print("   python backend/app.py")
    
    else:
        print("❌ System Status: DOWN")
        print("💡 Start the system with:")
        print("   python start_system.py")
        print("   or")
        print("   START_REACT_SYSTEM.bat")
    
    print()
    return backend_ok and frontend_ok

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)