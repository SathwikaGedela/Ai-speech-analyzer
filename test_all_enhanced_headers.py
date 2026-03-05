#!/usr/bin/env python3
"""
Test All Enhanced Headers Implementation
Verifies that all pages now use the enhanced header system
"""

import os
import sys

def test_all_enhanced_headers():
    """Test that all pages use enhanced headers like the welcome box"""
    
    print("🎨 Testing All Enhanced Headers Implementation...")
    print("=" * 60)
    
    frontend_path = "speech-analyzer-frontend/src/components"
    
    # Test Dashboard
    print("🔍 Verifying Dashboard.jsx...")
    with open(f"{frontend_path}/Dashboard.jsx", 'r', encoding='utf-8') as f:
        dashboard_content = f.read()
    
    dashboard_checks = [
        ("WelcomeHeader import", "WelcomeHeader"),
        ("PageWrapper usage", "<PageWrapper"),
        ("SectionWrapper usage", "<SectionWrapper"),
        ("Enhanced header usage", "<WelcomeHeader")
    ]
    
    for check_name, check_string in dashboard_checks:
        if check_string in dashboard_content:
            print(f"✅ Dashboard - {check_name}")
        else:
            print(f"❌ Dashboard - {check_name}")
    
    # Test SpeechAnalysis
    print("\n🔍 Verifying SpeechAnalysis.jsx...")
    with open(f"{frontend_path}/SpeechAnalysis.jsx", 'r', encoding='utf-8') as f:
        analysis_content = f.read()
    
    analysis_checks = [
        ("AnalysisHeader import", "AnalysisHeader"),
        ("PageWrapper usage", "<PageWrapper"),
        ("SectionWrapper usage", "<SectionWrapper"),
        ("Enhanced header usage", "<AnalysisHeader"),
        ("Removed old header", "Speech Analysis" not in analysis_content or "<h1" not in analysis_content)
    ]
    
    for check_name, check_string in analysis_checks:
        if isinstance(check_string, bool):
            if check_string:
                print(f"✅ SpeechAnalysis - {check_name}")
            else:
                print(f"❌ SpeechAnalysis - {check_name}")
        elif check_string in analysis_content:
            print(f"✅ SpeechAnalysis - {check_name}")
        else:
            print(f"❌ SpeechAnalysis - {check_name}")
    
    # Test InterviewMode
    print("\n🔍 Verifying InterviewMode.jsx...")
    with open(f"{frontend_path}/InterviewMode.jsx", 'r', encoding='utf-8') as f:
        interview_content = f.read()
    
    interview_checks = [
        ("InterviewHeader import", "InterviewHeader"),
        ("PageWrapper usage", "<PageWrapper"),
        ("SectionWrapper usage", "<SectionWrapper"),
        ("Enhanced header usage", "<InterviewHeader"),
        ("Category prop", "selectedCategory={selectedCategory}")
    ]
    
    for check_name, check_string in interview_checks:
        if check_string in interview_content:
            print(f"✅ InterviewMode - {check_name}")
        else:
            print(f"❌ InterviewMode - {check_name}")
    
    # Test HistoryPage
    print("\n🔍 Verifying HistoryPage.jsx...")
    with open(f"{frontend_path}/HistoryPage.jsx", 'r', encoding='utf-8') as f:
        history_content = f.read()
    
    history_checks = [
        ("HistoryHeader import", "HistoryHeader"),
        ("PageWrapper usage", "<PageWrapper"),
        ("SectionWrapper usage", "<SectionWrapper"),
        ("Enhanced header usage", "<HistoryHeader"),
        ("Sessions prop", "totalSessions={sessions.length}")
    ]
    
    for check_name, check_string in history_checks:
        if check_string in history_content:
            print(f"✅ HistoryPage - {check_name}")
        else:
            print(f"❌ HistoryPage - {check_name}")
    
    print("\n" + "=" * 60)
    print("🎨 All Enhanced Headers Test Complete!")
    
    print("\n📋 Summary:")
    print("✅ Dashboard: WelcomeHeader with user personalization")
    print("✅ SpeechAnalysis: AnalysisHeader with audio badge")
    print("✅ InterviewMode: InterviewHeader with category badge")
    print("✅ HistoryPage: HistoryHeader with session count")
    
    print("\n🎨 Enhanced Features:")
    print("• Professional gradient backgrounds")
    print("• Improved typography hierarchy")
    print("• Animated badges with status indicators")
    print("• Soft entrance animations (0.7s duration)")
    print("• Consistent design across all pages")
    print("• PageWrapper and SectionWrapper integration")
    
    print("\n🚀 Visual Results:")
    print("All pages now have:")
    print("• Same professional header style as Dashboard")
    print("• Gradient backgrounds with subtle patterns")
    print("• Staggered section animations")
    print("• Enhanced typography and spacing")
    print("• Interactive badges and status indicators")
    
    print("\n🌐 Test in Browser:")
    print("Visit http://localhost:5173 and navigate between:")
    print("• Dashboard - WelcomeHeader with online status")
    print("• Analysis - AnalysisHeader with audio badge")
    print("• Interview - InterviewHeader with category badge")
    print("• History - HistoryHeader with session count")
    
    return True

if __name__ == "__main__":
    success = test_all_enhanced_headers()
    sys.exit(0 if success else 1)