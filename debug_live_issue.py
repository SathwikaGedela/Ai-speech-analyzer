#!/usr/bin/env python3
"""
Debug the live Network error issue
"""

import sys
import os
import subprocess
import time
import threading

def monitor_backend():
    """Monitor backend output in real-time"""
    print("🔍 LIVE DEBUGGING - NETWORK ERROR")
    print("=" * 50)
    
    print("\n1️⃣ Starting Backend with Full Logging...")
    
    # Start backend with real-time output
    process = subprocess.Popen(
        [sys.executable, 'backend/app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    print("✅ Backend started - watching for errors...")
    print("🌐 Open browser to: http://127.0.0.1:5000")
    print("📝 Try to analyze audio and watch for errors below:")
    print("-" * 50)
    
    try:
        # Read output line by line
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"BACKEND: {line.strip()}")
                
                # Look for specific error patterns
                if "error" in line.lower():
                    print(f"🚨 ERROR DETECTED: {line.strip()}")
                elif "traceback" in line.lower():
                    print(f"🚨 TRACEBACK DETECTED: {line.strip()}")
                elif "exception" in line.lower():
                    print(f"🚨 EXCEPTION DETECTED: {line.strip()}")
                elif "POST /analyze" in line:
                    print(f"📡 ANALYZE REQUEST: {line.strip()}")
                    
    except KeyboardInterrupt:
        print("\n⏹️ Stopping backend...")
        process.terminate()
        process.wait()
        print("✅ Backend stopped")

if __name__ == "__main__":
    monitor_backend()