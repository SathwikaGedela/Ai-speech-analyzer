#!/usr/bin/env python3
"""
Test script to verify landing page spacing changes
"""

import os
import sys

def test_landing_page_spacing():
    """Test that landing page spacing has been reduced"""
    
    landing_page_path = "speech-analyzer-frontend/src/components/LandingPage.jsx"
    
    if not os.path.exists(landing_page_path):
        print("❌ Landing page file not found")
        return False
    
    with open(landing_page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check that py-24 has been replaced with py-12
    py_24_count = content.count('py-24')
    py_12_count = content.count('py-12')
    
    print(f"📊 Spacing Analysis:")
    print(f"   - py-24 (large spacing): {py_24_count} instances")
    print(f"   - py-12 (reduced spacing): {py_12_count} instances")
    
    # Check for other spacing improvements
    mb_20_count = content.count('mb-20')
    mb_16_count = content.count('mb-16')
    mb_12_count = content.count('mb-12')
    mb_8_count = content.count('mb-8')
    mb_6_count = content.count('mb-6')
    
    print(f"   - mb-20 (large margin): {mb_20_count} instances")
    print(f"   - mb-16 (large margin): {mb_16_count} instances") 
    print(f"   - mb-12 (medium margin): {mb_12_count} instances")
    print(f"   - mb-8 (small margin): {mb_8_count} instances")
    print(f"   - mb-6 (small margin): {mb_6_count} instances")
    
    # Check for gap reductions
    gap_16_count = content.count('gap-16')
    gap_12_count = content.count('gap-12')
    gap_8_count = content.count('gap-8')
    
    print(f"   - gap-16 (large gap): {gap_16_count} instances")
    print(f"   - gap-12 (medium gap): {gap_12_count} instances")
    print(f"   - gap-8 (small gap): {gap_8_count} instances")
    
    # Verify key sections have reduced spacing
    sections_with_py12 = [
        'section id="features" className="py-12',
        'section id="about" className="py-12',
        'section id="demo" className="py-12',
        'section className="py-12'  # CTA section
    ]
    
    sections_found = 0
    for section in sections_with_py12:
        if section in content:
            sections_found += 1
            print(f"✅ Found reduced spacing: {section}")
        else:
            print(f"❌ Missing reduced spacing: {section}")
    
    print(f"\n📈 Results:")
    print(f"   - Sections with reduced spacing: {sections_found}/4")
    print(f"   - Large py-24 spacing remaining: {py_24_count}")
    
    if sections_found == 4 and py_24_count == 0:
        print("✅ Landing page spacing successfully reduced!")
        return True
    else:
        print("⚠️  Some spacing issues may remain")
        return False

if __name__ == "__main__":
    success = test_landing_page_spacing()
    sys.exit(0 if success else 1)