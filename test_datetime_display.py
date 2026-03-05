#!/usr/bin/env python3
"""
Test datetime display by making a request to the history page
"""

import requests
import re

def test_datetime_display():
    """Test the datetime display in the history page"""
    
    print("🕐 TESTING DATETIME DISPLAY")
    print("=" * 40)
    
    try:
        # Get the history page
        response = requests.get("http://127.0.0.1:5000/history", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            print("✅ History page loaded successfully")
            
            # Extract date/time entries from the table
            # Look for table rows with date patterns
            date_pattern = r'<td>([^<]+)</td>'
            matches = re.findall(date_pattern, content)
            
            print(f"\n📅 FOUND DATE/TIME ENTRIES:")
            date_entries = []
            for match in matches:
                # Skip non-date entries (like transcript previews, numbers, etc.)
                if any(month in match for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']) or \
                   any(char.isdigit() and ('-' in match or ',' in match) for char in match):
                    date_entries.append(match.strip())
            
            if date_entries:
                for i, date_entry in enumerate(date_entries[:5], 1):  # Show first 5
                    print(f"   {i}. {date_entry}")
                
                print(f"\n✅ Found {len(date_entries)} date entries")
                print("📝 Format appears to be working!")
            else:
                print("⚠️ No clear date entries found in table")
                print("This might mean the formatting needs adjustment")
            
            # Check for any error messages in the page
            if "error" in content.lower() or "exception" in content.lower():
                print("❌ Possible errors detected in page content")
            else:
                print("✅ No errors detected in page content")
                
        else:
            print(f"❌ History page error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing datetime display: {e}")
    
    print("\n" + "=" * 40)
    print("💡 EXPECTED FORMAT:")
    print("   '27 Dec 2025, 10:30' (friendly format)")
    print("   'December 27, 2025 at 10:30 AM' (full format)")

if __name__ == "__main__":
    test_datetime_display()