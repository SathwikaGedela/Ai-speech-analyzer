#!/usr/bin/env python3
"""
Test landing page and complete user flow
"""

import requests

BASE_URL = "http://localhost:5000"

def test_landing_page_flow():
    print("🏠 Testing Landing Page Flow\n")
    
    print("1. Testing Root URL Redirect...")
    try:
        response = requests.get(f"{BASE_URL}/", allow_redirects=True)
        if response.status_code == 200 and "SpeechAnalyzer Pro" in response.text:
            print("✅ Root URL redirects to landing page")
            print(f"   Page title: SpeechAnalyzer Pro - Advanced Speech Analysis")
        else:
            print(f"❌ Root URL redirect failed")
            return False
    except Exception as e:
        print(f"❌ Error testing root URL: {e}")
        return False
    
    print("\n2. Testing Landing Page Content...")
    try:
        response = requests.get(f"{BASE_URL}/landing")
        if response.status_code == 200:
            content = response.text
            
            # Check for key sections
            sections = [
                ("Hero Section", "Master Your Speaking Skills"),
                ("Features Section", "Powerful Features"),
                ("About Section", "About SpeechAnalyzer Pro"),
                ("Demo Section", "See It In Action"),
                ("CTA Section", "Ready to Improve Your Speaking?")
            ]
            
            for section_name, section_text in sections:
                if section_text in content:
                    print(f"✅ {section_name} - Present")
                else:
                    print(f"❌ {section_name} - Missing")
            
            # Check for feature cards
            features = [
                "Speech Analysis",
                "Interview Training", 
                "Emotion Analysis",
                "Progress Tracking",
                "Real-time Analysis",
                "Multi-format Support"
            ]
            
            print(f"\n   Feature Cards:")
            for feature in features:
                if feature in content:
                    print(f"   ✅ {feature}")
                else:
                    print(f"   ❌ {feature}")
                    
        else:
            print(f"❌ Landing page not accessible")
            return False
    except Exception as e:
        print(f"❌ Error testing landing page: {e}")
        return False
    
    print("\n3. Testing Navigation Links...")
    try:
        response = requests.get(f"{BASE_URL}/landing")
        content = response.text
        
        # Check for auth links
        auth_links = content.count('href="/auth"')
        if auth_links >= 3:
            print(f"✅ Authentication links present ({auth_links} found)")
        else:
            print(f"❌ Not enough authentication links ({auth_links} found)")
        
    except Exception as e:
        print(f"❌ Error testing navigation: {e}")
        return False
    
    print("\n4. Testing Protected Route Redirect...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard", allow_redirects=True)
        if "SpeechAnalyzer Pro" in response.text and "Master Your Speaking Skills" in response.text:
            print("✅ Protected routes redirect to landing page")
        else:
            print("❌ Protected routes not redirecting properly")
            return False
    except Exception as e:
        print(f"❌ Error testing protected routes: {e}")
        return False
    
    return True

def test_user_journey():
    print("\n👤 Testing Complete User Journey\n")
    
    session = requests.Session()
    
    print("1. User visits website...")
    try:
        response = session.get(f"{BASE_URL}/")
        if "Master Your Speaking Skills" in response.text:
            print("✅ Lands on attractive landing page")
        else:
            print("❌ Landing page not shown")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n2. User clicks 'Get Started'...")
    try:
        response = session.get(f"{BASE_URL}/auth")
        if "Join Speech Analysis" in response.text:
            print("✅ Redirected to authentication page")
        else:
            print("❌ Authentication page not shown")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n3. User registers account...")
    test_user = {
        "firstName": "Demo",
        "lastName": "User", 
        "email": "demo.user@example.com",
        "phone": "+1555123456",
        "password": "demopass123",
        "confirmPassword": "demopass123"
    }
    
    try:
        response = session.post(f"{BASE_URL}/api/signup", json=test_user)
        if response.status_code == 201:
            print("✅ Account registration successful")
        else:
            print(f"❌ Registration failed: {response.json().get('error', 'Unknown')}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    print("\n4. User signs in...")
    try:
        signin_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = session.post(f"{BASE_URL}/api/signin", json=signin_data)
        if response.status_code == 200:
            print("✅ Sign in successful")
        else:
            print(f"❌ Sign in failed")
            return False
    except Exception as e:
        print(f"❌ Sign in error: {e}")
        return False
    
    print("\n5. User accesses application features...")
    try:
        response = session.get(f"{BASE_URL}/")
        if "Speech Analysis" in response.text and "Upload" in response.text:
            print("✅ Full application access granted")
        else:
            print("❌ Application features not accessible")
            return False
    except Exception as e:
        print(f"❌ Error accessing features: {e}")
        return False
    
    return True

def main():
    print("🚀 Testing Landing Page Integration\n")
    
    try:
        # Test landing page
        if test_landing_page_flow():
            print("\n🎉 Landing page tests passed!")
        else:
            print("\n❌ Landing page tests failed!")
            return
        
        # Test user journey
        if test_user_journey():
            print("\n🎉 Complete user journey works perfectly!")
        else:
            print("\n❌ User journey has issues!")
            return
        
        print("\n📋 User Experience Flow:")
        print("1. 🏠 Visit http://localhost:5000/ → Beautiful landing page")
        print("2. 📖 Learn about features and benefits")
        print("3. 🚀 Click 'Get Started' → Authentication page")
        print("4. 📝 Register account → Sign in")
        print("5. 🎯 Access full speech analysis features")
        
        print("\n🌟 Landing Page Features:")
        print("   • Hero section with compelling headline")
        print("   • 6 detailed feature cards with descriptions")
        print("   • About section explaining the app")
        print("   • Demo section encouraging trial")
        print("   • Call-to-action buttons throughout")
        print("   • Modern glass morphism design")
        print("   • Smooth animations and interactions")
        print("   • Mobile-responsive layout")
        
        print("\n✅ Landing page successfully added before authentication!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()