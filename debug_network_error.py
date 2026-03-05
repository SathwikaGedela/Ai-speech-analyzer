#!/usr/bin/env python3
"""
Debug the "Network error" issue in the web interface
"""

import sys
import os
import subprocess
import time
import requests
import json

def debug_network_error():
    print("🔍 DEBUGGING 'Network error' ISSUE")
    print("=" * 50)
    
    # Start the backend
    print("\n1️⃣ Starting Backend...")
    process = subprocess.Popen(
        [sys.executable, 'backend/app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for startup
    time.sleep(3)
    
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print("❌ Backend failed to start")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        return
    
    print("✅ Backend started")
    
    try:
        # Test 1: Check if main page loads
        print("\n2️⃣ Testing Main Page...")
        response = requests.get('http://127.0.0.1:5000', timeout=5)
        print(f"✅ Main page status: {response.status_code}")
        
        # Test 2: Test analyze endpoint with minimal data
        print("\n3️⃣ Testing Analyze Endpoint...")
        
        # Create a minimal test file
        test_content = b"fake audio content for testing"
        files = {'audio_file': ('test.wav', test_content, 'audio/wav')}
        
        try:
            response = requests.post('http://127.0.0.1:5000/analyze', files=files, timeout=10)
            print(f"✅ Analyze endpoint status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ JSON response received: {data.get('success', 'unknown')}")
                except:
                    print("⚠️ Response is not JSON")
                    print(f"Response text: {response.text[:200]}...")
            else:
                print(f"❌ Error response: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out - this could cause 'Network error'")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - this could cause 'Network error'")
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        # Test 3: Check backend logs
        print("\n4️⃣ Checking Backend Logs...")
        
        # Get some output from the process
        try:
            # Send a simple request to generate logs
            requests.get('http://127.0.0.1:5000', timeout=2)
            time.sleep(1)
        except:
            pass
        
        print("Check the terminal where you ran 'python backend/app.py' for error messages")
        
    finally:
        # Clean up
        process.terminate()
        process.wait()
        print("\n✅ Backend stopped")
    
    # Test 4: Common issues
    print("\n5️⃣ COMMON CAUSES OF 'Network error':")
    print("-" * 30)
    
    issues = [
        "🔍 Backend not running (run: python backend/app.py)",
        "🔍 Wrong port (should be http://127.0.0.1:5000)",
        "🔍 Missing dependencies (check requirements.txt)",
        "🔍 File upload too large (check file size)",
        "🔍 Audio processing error (check FFmpeg installation)",
        "🔍 Speech recognition timeout (Google API issue)",
        "🔍 Browser blocking localhost requests",
        "🔍 Antivirus/firewall blocking connection"
    ]
    
    for issue in issues:
        print(f"   {issue}")
    
    print("\n6️⃣ DEBUGGING STEPS:")
    print("-" * 30)
    
    steps = [
        "1. Open browser developer tools (F12)",
        "2. Go to Network tab",
        "3. Try to analyze audio",
        "4. Check if /analyze request appears",
        "5. Click on the request to see error details",
        "6. Check Console tab for JavaScript errors"
    ]
    
    for step in steps:
        print(f"   {step}")

if __name__ == "__main__":
    debug_network_error()