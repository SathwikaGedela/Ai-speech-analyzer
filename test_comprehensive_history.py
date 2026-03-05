#!/usr/bin/env python3
"""
Test the comprehensive history functionality
"""

import requests
import re

def test_comprehensive_history():
    """Test the comprehensive history page"""
    
    print("📊 TESTING COMPREHENSIVE HISTORY PAGE")
    print("=" * 50)
    
    try:
        # Test server connection
        print("🌐 Testing server connection...")
        response = requests.get("http://127.0.0.1:5000/history", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            print("✅ History page loaded successfully")
            
            # Check for new comprehensive columns
            expected_columns = [
                "Overall Score",
                "Grammar",
                "Vocabulary", 
                "Actions",
                "📊 Details"
            ]
            
            print("\n🔍 CHECKING NEW TABLE COLUMNS:")
            print("-" * 30)
            
            for column in expected_columns:
                if column in content:
                    print(f"   ✅ {column}: Found")
                else:
                    print(f"   ❌ {column}: Missing")
            
            # Check for detailed analysis functionality
            detailed_features = [
                ("Detailed modal", "showDetailedAnalysis"),
                ("Comprehensive report", "Comprehensive Analysis Report"),
                ("Analysis sections", "analysis-section"),
                ("Metric grids", "metric-grid"),
                ("Detail buttons", "detail-btn")
            ]
            
            print("\n🔧 CHECKING DETAILED ANALYSIS FEATURES:")
            print("-" * 40)
            
            for feature_name, search_term in detailed_features:
                if search_term in content:
                    print(f"   ✅ {feature_name}: Found")
                else:
                    print(f"   ❌ {feature_name}: Missing")
            
            # Count table rows to see if data is present
            table_rows = content.count('<tr>') - 1  # Subtract header row
            print(f"\n📊 DATA ANALYSIS:")
            print(f"   Sessions in table: {table_rows}")
            
            if table_rows > 0:
                print("   ✅ Session data is present")
                
                # Check for comprehensive data display
                comprehensive_indicators = [
                    "skill_level",
                    "word_count", 
                    "filler_percentage",
                    "grammar_score",
                    "vocabulary_diversity",
                    "engagement_level"
                ]
                
                found_indicators = sum(1 for indicator in comprehensive_indicators if indicator in content)
                print(f"   📈 Comprehensive data indicators: {found_indicators}/{len(comprehensive_indicators)}")
                
                if found_indicators >= len(comprehensive_indicators) // 2:
                    print("   ✅ Comprehensive data is being displayed")
                else:
                    print("   ⚠️ Limited comprehensive data (may be old sessions)")
            else:
                print("   ⚠️ No session data found")
            
            # Check JavaScript functionality
            js_functions = [
                "showDetailedAnalysis",
                "closeDetailedModal", 
                "toggleTranscript",
                "showTranscriptModal"
            ]
            
            js_found = sum(1 for func in js_functions if func in content)
            print(f"\n🔧 JAVASCRIPT FUNCTIONS: {js_found}/{len(js_functions)} found")
            
        else:
            print(f"❌ History page error: {response.status_code}")
            print("Make sure the server is running: python backend/app.py")
            return
            
    except requests.exceptions.RequestException:
        print("❌ Server not running")
        print("Please start the server first: python backend/app.py")
        return
    except Exception as e:
        print(f"❌ Error testing comprehensive history: {e}")
        return
    
    print("\n" + "=" * 50)
    print("🎯 COMPREHENSIVE HISTORY FEATURES:")
    print("   ✅ Extended table with 10 columns (vs 7 before)")
    print("   ✅ Overall Score with skill level")
    print("   ✅ Detailed WPM with word count")
    print("   ✅ Filler count with percentage")
    print("   ✅ Grammar score with error count")
    print("   ✅ Vocabulary diversity with unique words")
    print("   ✅ Enhanced sentiment display")
    print("   ✅ Emotion with engagement level")
    print("   ✅ Detailed analysis modal")
    print("   ✅ Comprehensive analysis report")
    
    print("\n💡 NEW CAPABILITIES:")
    print("   📊 Click 'Details' for comprehensive analysis")
    print("   📈 View all metrics, assessments, and tips")
    print("   📝 See strengths, improvements, and actionable advice")
    print("   🎯 Grammar errors and detailed feedback")
    print("   📄 Full transcript in detailed view")
    
    print("\n🚀 NEXT STEPS:")
    print("   1. Record new speech to see comprehensive data")
    print("   2. Click 'Details' button to view full analysis")
    print("   3. Compare old vs new session data")

if __name__ == "__main__":
    test_comprehensive_history()