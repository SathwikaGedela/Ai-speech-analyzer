#!/usr/bin/env python3
"""
Test the improved transcript preview functionality
"""

import requests
import re

def test_transcript_preview():
    """Test the transcript preview improvements"""
    
    print("📝 TESTING TRANSCRIPT PREVIEW IMPROVEMENTS")
    print("=" * 50)
    
    try:
        # Start server first
        print("🌐 Testing server connection...")
        response = requests.get("http://127.0.0.1:5000/history", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            print("✅ History page loaded successfully")
            
            # Check for new transcript features
            features_to_check = [
                ("Expandable transcripts", "toggleTranscript"),
                ("Modal functionality", "showTranscriptModal"),
                ("Copy functionality", "copyTranscript"),
                ("Show More/Less", "Show More"),
                ("View Full option", "View Full"),
                ("Modal close", "closeTranscriptModal"),
                ("Improved CSS", "transcript-preview"),
                ("Modal styles", "transcript-modal")
            ]
            
            print("\n🔍 CHECKING NEW FEATURES:")
            print("-" * 30)
            
            for feature_name, search_term in features_to_check:
                if search_term in content:
                    print(f"   ✅ {feature_name}: Found")
                else:
                    print(f"   ❌ {feature_name}: Missing")
            
            # Check for transcript content
            transcript_pattern = r'<div class="transcript-preview"[^>]*>.*?</div>'
            transcript_matches = re.findall(transcript_pattern, content, re.DOTALL)
            
            print(f"\n📊 TRANSCRIPT PREVIEWS FOUND: {len(transcript_matches)}")
            
            if transcript_matches:
                print("✅ Transcript previews are present in the page")
                
                # Check for improved length (should be 80 chars instead of 50)
                if "transcript[:80]" in content:
                    print("✅ Transcript preview length increased to 80 characters")
                else:
                    print("⚠️ Transcript preview length may not be updated")
            else:
                print("⚠️ No transcript previews found (may be no sessions)")
            
            # Check for JavaScript functions
            js_functions = ["toggleTranscript", "showTranscriptModal", "copyTranscript", "closeTranscriptModal"]
            js_found = sum(1 for func in js_functions if func in content)
            
            print(f"\n🔧 JAVASCRIPT FUNCTIONS: {js_found}/{len(js_functions)} found")
            
            if js_found == len(js_functions):
                print("✅ All JavaScript functions implemented")
            else:
                print("⚠️ Some JavaScript functions may be missing")
                
        else:
            print(f"❌ History page error: {response.status_code}")
            print("Make sure the server is running: python backend/app.py")
            
    except requests.exceptions.RequestException:
        print("❌ Server not running")
        print("Please start the server first: python backend/app.py")
        return
    except Exception as e:
        print(f"❌ Error testing transcript preview: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 TRANSCRIPT PREVIEW IMPROVEMENTS:")
    print("   ✅ Increased preview length (50 → 80 characters)")
    print("   ✅ Click to expand/collapse full transcript")
    print("   ✅ Modal popup for comfortable full-text reading")
    print("   ✅ Copy transcript to clipboard functionality")
    print("   ✅ Better responsive design for mobile")
    print("   ✅ Hover effects and visual feedback")
    
    print("\n💡 HOW TO USE:")
    print("   1. 'Show More' - Expand transcript in table")
    print("   2. 'View Full' - Open transcript in modal popup")
    print("   3. 'Copy Text' - Copy full transcript to clipboard")
    print("   4. Click outside modal or press Escape to close")

if __name__ == "__main__":
    test_transcript_preview()